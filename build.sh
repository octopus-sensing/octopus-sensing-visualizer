#!/bin/bash

cd ui/
npm install
npm run build-prod

cd ../server/
cp ../README.md .
poetry install
poetry build

read -p "Publish to PyPi? [y/N]" -e answer
if [ $answer == "y" -o $answer == "Y" ]
then
  poetry publish
fi

rm README.md
