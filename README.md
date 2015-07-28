# yoda-api
Translate to Yodish, you can.

In 2015 [Enspiral Dev Academy](http://devacademy.co.nz) students noticed the [Yoda Speak](https://www.mashape.com/ismaelc/yoda-speak) API wasn't working so well.

I thought to myself, "People *need* reliable translations to the Yodish!"

Source material: http://www.yodajeff.com/pages/talk/yodish.shtml

## Usage

Submit a GET request to http://yoda-api.appspot.com/api/v1/yodish with the urlencoded string in the `text` querystring parameter. For example:

    http://yoda-api.appspot.com/api/v1/yodish?text=I%20am%20a%20little%20green%20alien

yields the following JSON:

    {
        "yodish": "A little green alien, I am."
    }

I'd prefer it if you didn't spam requests... the external part of speech tagger only provides 1000 free requests an hour, and I haven't implemented rate limiting yet!

(As it turns out, NLTK is annoying to deploy to App Engine because only pure Python modules are supported. I 'outsourced' tagging to text-processing.com.)

## It's not easy, being green

I wouldn't even say I'm that much of a Star Wars junkie, but as it turns out, talking like Yoda is quite an interesting natural language processing task. Mostly because he's inconsistent! It's hard to find rules that *always* apply. Here's a sample of his dialogue from The Empire Strikes Back "Dagobah System" scenes:

    Away put your weapon. I mean you no harm. I am wondering: why are you here?

    Looking? Found someone you have I would say.

    Help you I can. Yes. Mmmmm.

    Great warrior? Wars not make one great!

    How you get so big eating food of this kind?

    Mine! Or I will help you not.

    Mudhole? Slimy? My home this is!

    Stay and help you I will.

    Take you to him, I will.

    Use the force. Yes.

    Size matters not. Look at me. Judge me by my size, do you? And well you should not. For my ally is the force. And a powerful ally it is.

    So certain are you?

    For the Jedi it is time to eat as well.

    Powerful Jedi was he.

    I cannot teach him. The boy has no patience.

    Much anger in him. Like his father.

    He is not ready.

    Ready, are you? What know you of 'ready'?

    For eight hundred years have I trained Jedi. My own counsel will I keep on who is to be trained.

He says, *"He is not ready."* Why doesn't he say, *"Ready, he is not?"* Short of randomising the frequency of certain rearrangements, I've opted to make the API more consistent than Yoda himself.

## What works

There's a great deal of room for improvement. Only a few rules are currently implemented. What will work:

    I sense much anger in him. -> Much anger in him I sense.

    I am, You are -> get sent to end with a comma -> Angry, you are.

    Put away your weapons -> Away put your weapons.

Anything complex will almost certainly break. Multiple simple sentences work though.


