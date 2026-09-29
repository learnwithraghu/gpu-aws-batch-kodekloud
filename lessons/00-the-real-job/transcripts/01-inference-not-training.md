# Video 01 — Inference, not training
**Type:** Theory
**Runtime target:** ~3 minutes

---

Hello. Let's start with the product this course is built for.

KodeFood is a fast-food delivery app. Millions of people order from it. More than two thousand vendors are live, and more join every day. One of the hard parts is the photo a vendor uploads for a menu item. Someone still opens that picture and decides whether it looks like food worth showing. That does not scale.

So here's the design. We do not train a model on each vendor's menu. We run a finished caption model. The model writes one short sentence about the photo. If that sentence is about food, we accept the photo and keep the sentence as catalog text. If the sentence is about a car, a selfie, or a logo, we reject the photo. Nobody on the team had to open it. That catches obvious bad uploads. It does not prove the burger in the picture is the burger on the menu.

That work is inference, not training. Training is when the weights still move. You show the model labeled examples and nudge the weights. Inference is when the model is already finished. You hand it a photo and it hands you a caption. The weights at the end of a photo are the same weights you started with. The GPU just repeats the forward pass, about eight photos at a time so they fit in memory. Those eight are not eight catalogs. They are rows in one file, each with a caption and an accepted or rejected status.

Next is why that forward pass wants a GPU. A photo is a big grid of numbers, and a caption is a lot of the same math on that grid.
