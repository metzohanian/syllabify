#!/bin/bash

docker stop syllabify && docker rm syllabify
docker build -t tempotalk:syllabify -f Dockerfile .
docker run -dit --name syllabify -v ~/Development/solutionmachine/tempotalk/syllabify:/var/syllabify tempotalk:syllabify