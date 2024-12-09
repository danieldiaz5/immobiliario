FROM baseImage
EXPOSE 80


# Installar módulos necesarios 
RUN pip install -r requierements.txt

CMD [ "python","main.py" ]