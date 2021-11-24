# Paraphrase Server

[![Run on Ainize](https://ainize.ai/images/run_on_ainize_button.svg)](https://ainize.web.app/redirect?git_repo=https://github.com/imjeffhi4/ainize-paraphrase-app)

A FastAPI implementation of a fine-tuned T5 model that generates paraphrases. 

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

![Untitled](Paraphrase%20Server%20f294c40523ae4c908e7548b15b2de07e/Untitled.png)
