#!/bin/bash

strings recurso/Capture.pcapng | grep HTTP | grep GET
#pip install -U oletools #si no esta la tool
olevba recurso/Monke.xlsm > recurso/macros.txt
cat recurso/macros.txt | grep -i flag

#Llamado a la receta con los datos necesarios
# https://gchq.github.io/CyberChef/#recipe=Find_/_Replace(%7B'option':'Simple%20string','string':'-'%7D,'%20',true,false,true,false)From_Decimal('Space',false)XOR(%7B'option':'UTF8','string':'MonkeyMagic'%7D,'Standard',false)&input=CQkJCQkJCTExLTMtMTUtMTItOTUtODktOS01Mi0zNi02MS0zNy01NC0zNC05MC0xNS04Ni0zOC0yNi04MC0xOS0xLTYwLTEyLTM4LTQ5LTktMjgtMzgtMC04MS05LTItODAtNTItMjgtMTk&ieol=CRLF&oeol=FF

