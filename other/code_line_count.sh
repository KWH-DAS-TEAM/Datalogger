#!/bin/bash
find /kwh/* ! -path '/kwh/lib*' -a ! -path '/kwh/other*' -a ! -path '/kwh/UNLIC*' -a ! -path "*.log" -name '*' ! -path "/kwh/helpful_pdfs/*" | xargs wc -l

