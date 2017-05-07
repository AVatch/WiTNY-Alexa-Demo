# WITNY 2017 Build-a-thon Sample Skill

## Quick Links
- [Amazon Alexa Web Portal](https://alexa.amazon.com)
- [Amazon Developer Alexa Portal](https://developer.amazon.com/alexa-skills-kit)
- [Amazon Intent Slot Type Ref](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/built-in-intent-ref/slot-type-reference)

## Resources
- [flask-ask](https://whydoesitsuck.com/top-five-most-annoying-programming-languages/)
- [Amazon + flask-ask Intro](https://developer.amazon.com/blogs/post/Tx14R0IYYGH3SKT/Flask-Ask-A-New-Python-Framework-for-Rapid-Alexa-Skills-Kit-Development)
- [ngrok](https://ngrok.com/)
- [NodeJS Alexa Skillkit](https://github.com/alexa/alexa-skills-kit-sdk-for-nodejs)
- [Example of Skill written in Node (work in prog. see various branches)](https://github.com/nbuhay/alexa-helloWorld) 

## Quick Overview of Building a Skill
You can think of an Alexa Skill as an app for a smartphone, except the primary interface is speech/voice. While apps can provide a visually rich interface, they require the user's active attention (for the most part). On the other hand, Alexa skills tend to be hands free and quick bursts of information. 

In the simplest sense we can think of Alexa skills in a similiar way as we think about REST APIs. With Alexa, the Echo Dot, or Alexa-enabled device, is the client which consumes your Skill's API. 

1. ```Utterances``` -> ```Urls```
2. ```Interaction Model``` -> ```Url Mapping```
3. ```Intents``` -> ```The functions which handle requests```

#### Utterances
A set of likely spoken phrases mapped to the intents. This should include as many representative phrases as possible.

In the above example the utterances are:
```
AddContactInitIntent add to contact
AddContactNameIntent {name}
AddContactNumberIntent Their number is {number}
AddToContactBookConfirmIntent {name} {number}
SendToContactIntent Send {name} {query}
```
These are the phrases Alexa will be monitoring for while the skill is active. Anything inside of the curly brackets is a data type variable which will be parsed and passed along to the function handling that intent.


#### Interaction Model
A structure that identifies the steps for a multi-turn conversation between your skill and the user to collect all the information needed to fulfill each intent. This simplifies the code you need to write to ask the user for information.

In the above example the interaction model is: 
```
{
  "intents": [
    {
      "intent": "AddContactInitIntent"
    },
    {
      "slots": [
        {
          "name": "name",
          "type": "LIST_OF_NAMES"
        }
      ],
      "intent": "AddContactNameIntent"
    },
    {
      "slots": [
        {
          "name": "number",
          "type": "AMAZON.NUMBER"
        }
      ],
      "intent": "AddContactNumberIntent"
    },
    {
      "slots": [
        {
          "name": "name",
          "type": "LIST_OF_NAMES"
        },
        {
          "name": "number",
          "type": "AMAZON.NUMBER"
        }
      ],
      "intent": "AddToContactBookConfirmIntent"
    },
    {
      "slots": [
        {
          "name": "name",
          "type": "LIST_OF_NAMES"
        },
        {
          "name": "query",
          "type": "AMAZON.Animal"
        }
      ],
      "intent": "SendToContactIntent"
    }
  ]
}
```

We can see that the model maps an ```Intent``` to an array of ```slots```. The ```slots``` are a representative list of possible values. Custom slot types are used for lists of items that are not covered by one of Amazon’s built-in slot types. [Here](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/built-in-intent-ref/slot-type-reference) is the list of built in slot types provided by Amazon.

To create a custom ```slot``` type like we have above with ```LIST_OF_NAMES``` we need to provide Amazon witgh a newline seperated list of possible values. In our case, it is simply: 

```
Adrian
James
Scott
Arnaud
Stephen
```

#### Intents
An intent represents an action that fulfills a user’s spoken request. Intents can optionally have arguments called slots. Intents are specified in a JSON structure called the intent schema.

We can call our ```intents``` whatever we want. When we define the function to handle these intents in our flask app, we must decorate the function with the appropriate ```@ask``` decorator.

```
@ask.intent("AddContactNameIntent", convert={'name': str})
def prompt_new_contact_number(name):
    session.attributes['name'] = name
    msg = render_template('prompt_for_number', name=name)
    return question(msg)
```

The above function does a few things. It first maps the ```AddContactNameIntent``` we defined in the Interaction Model to the ```prompt_new_contact_number``` function. It passes along the ```name``` slot value as a parameter to the function as well and declares its data type. These functions must all return a response which can be of the ```question``` or ```statement``` form, much like how a REST API must return some type of response. 

```question``` responses expect the user to input a new command, therefore the application Alexa Skill session persists. 

```statement``` responses do not expect further input so after they are done the Alexa Skill session ends. 

Both the above respones expect either a ```string``` input or an identifier to a template in the ```templates.yaml``` file. This file defines the templates in basic ```jinja``` templating syntax. For more see [here](http://jinja.pocoo.org)

In this example we make use of the ```session``` object which is a session-only layer of persistance. We can use this object to share data and maintain state throughout the skill session. 

Here is the template used for the aboce ```intent```:

```
prompt_for_number: What is {{ name }} phone number?
```



To write to the ```session```:
```
session.attributes[KEY] = VALUE
```

To read from the ```session```:
```
foo = session.attributes[KEY]
```

Of course you can make use of a databse (as simple as a JSON file to complex as postgres).



## A Set of Useful API Sources (in no particular order)
- [NYC Open Data](https://opendata.cityofnewyork.us/data/): API for NYC public data
- [Twilio](https://www.twilio.com/docs/api/rest): API For automating SMS and Calls
- [Braintree](https://developers.braintreepayments.com/): API for automating payments (and sandbox/testing payments)
- [Sendgrid](https://sendgrid.com/docs/API_Reference/index.html): API for automating emails
- [Watson](https://developer.ibm.com/watson/): API for Machine Learning / NLP
- [Clarifai](https://www.clarifai.com/): Image and Video Recognition API
- [Google Maps](https://developers.google.com/maps/): Mappign API
- [Giphy](https://github.com/Giphy/GiphyAPI): API for searching Gifs
- [Auth0](https://auth0.com/): Authentication API
- [New York Times](https://developer.nytimes.com/): API for news
- [Weather Underground](https://www.wunderground.com/weather/api/): API for weather
- [Foursquare](https://developer.foursquare.com/): API for venues
- [Meetup](https://www.meetup.com/meetup_api/): API for events

