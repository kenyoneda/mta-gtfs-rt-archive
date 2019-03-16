#!/bin/bash
# Recursivley deletes empty directories in 'data' folder
find data -mindepth 1 -type d -empty -delete
