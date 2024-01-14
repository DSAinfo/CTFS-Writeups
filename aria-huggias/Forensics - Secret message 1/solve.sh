#!/bin/bash
pdf2txt secret.pdf | grep -o 'uoftctf{[^}]*}'
