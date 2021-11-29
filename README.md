# Paraphrase Server

A FastAPI implementation of a fine-tuned T5 model that generates paraphrases. If you'd like to demo this project, you can do so [here](https://finished-ainize-paraphrase-app-imjeffhi4.endpoint.ainize.ai/). If you'd like a more in-depth overview of how it works, check out my [blog post](https://medium.com/@imjeffhi4/creating-a-paraphrase-generator-model-using-t5-and-deploying-on-ainize-7742bc83532a) on Medium. 

# How to run

Building docker image:

```docker
docker build --no-cache -t paraphrase .
```

You can then run with:

```docker
docker run -p 8000:8000 paraphrase
```

# Using the WebApp

To use the web app, navigate to [localhost:8000](http://localhost:8000) in your browser. You may then use the sliders to vary how much you want the model to *attempt* to vary the original text. 

![https://i.ibb.co/JyxTKrp/ezgif-6-06f407acb047.gif](https://i.ibb.co/JyxTKrp/ezgif-6-06f407acb047.gif)
