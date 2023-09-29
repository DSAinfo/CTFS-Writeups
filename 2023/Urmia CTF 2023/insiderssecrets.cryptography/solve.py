import base64

txt = "Vm14V1QxWldTblZqTTJoWlpXeEtNRmRJY0VaTlIwWTJWRzFhYTFaRmNEQlVWbEpUVDFFOVBRPT0="
for x in range(0, 4):
    txt = base64.b64decode(txt)

print(txt) 
