pugpexxix
=========

metaprogramming code used at xxix pugpe encounter

from my point of view, metaprogramming can be used for three things:

1. syntactic sugar
1. create mini domain specific languages (which is syntactic sugar at its peak)
1. hijacking third party code 
1. aspect oriented programming

looking to this list, I can see the value of things going down as you
go up, with the costs surpassing the benefits at some point around
mini dsls and pure syntactc sugar.

the costs of doing metaprogramming, obviously, is manutenability.

so, take a look at the classes here, this is the designed way of doing this:

look at events modules
----------------------

events and events2 shows how to use some class decorators and inspection
to hook callbacks and events seamlessly.

events3 shows how I see this can be done nicer without making conventions
explicit.

take your time at minidsl modules
---------------------------------

minidsl shows how to use metaclass and descriptors to create simple
object validations. It also wire up some code in strings and execute it
to clean up method signature.

minidsl2 shows how to do the same black magic without metaclasses, and
exec, at the expenses of a little repetition.

learn true black magic at blackart module
-----------------------------------------

black art module shows how to hook up into python's importer system and
decorate every callable with some logging feature.

this way, (almost) any thin you import afterwards display these features
without you needing to change a line of code on it.

seek further knowledge
------------------------

learn more about aspected oriented programming and its predecessors to 
have a more clear idea of how to use metaprogramming properly.

__short hint: if it is your business logic, and you are using metaprogramming,
you're probably gonna have a bad time. __
