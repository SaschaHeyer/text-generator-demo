# Text generator demo

This is a smallm repository for a web app showcasing text-generators in multiple languages. The app is a starlette web-app and its based on the starter app recommended by [fastai](https://course.fast.ai/deployment_aws_beanstalk.html) available to [download](https://github.com/fastai/course-v3/raw/master/docs/production/aws-beanstalk.zip).

The English model for prediction is an AWD-LSTM architecture using a [pretrained model](https://docs.fast.ai/text.models.html) on [WikiText-103](https://www.salesforce.com/products/einstein/ai-research/the-wikitext-dependency-language-modeling-dataset/). 

The Spanish model is trained by myself on WikiText-103, and it's code is available [here](https://github.com/cduguet/ulmfit-es). 

# To-Do

A List of nice-to-have improvements I'd like to integrate in the future include but are not limited to: 

- Using prediction with beam search
- Fine-Tune on a specific topic dataset (probably Fashion or Legal)
- Train a BERT architecture
- Train a German Network
