# Video 03 — Mutable latest
**Type:** Theory
**Runtime target:** ~3 minutes

---

Alright. Let's talk about mutable latest.

The tag latest means whatever was pushed most recently to that tag. In this course the URI ends in gpu-teaching:latest, so the job definition is asking ECR for the current target of latest, not for a frozen build. The tag is a movable label. The digest underneath it stays immutable. What changes is which digest the label names.

That is convenient for teaching. You rebuild the image, you push, you submit, and the next job picks up the new code without anyone editing the job definition. The URI can stay your account id, then .dkr.ecr.ap-northeast-1.amazonaws.com/gpu-teaching:latest, for the whole course. A script change in photos.py or describe_items.py can ride that same tag. You do not register a new definition just to point at a new string. For KodeFood that means a caption fix can ship to the next vendor folder without rewriting the Batch contract.

It is also easy to surprise yourself. Mutable latest means whatever was pushed last. If you push a broken image and then submit, the next job pulls the broken one. A job that already started keeps the image it pulled. It does not jump to your newer push mid-run. The following job is the one that sees the new digest.

Production teams often refuse that surprise. When they need yesterday's successful job reproduced exactly, they pin a digest, or they pin an immutable version tag such as v3 or a git sha. An incident replay sounds like this: run this sha256 again. The digest is the precise bytes. The tag, if it can move, is only a nickname.

Picture the definition registered once with that latest URI. On Thursday you fix a caption bug, rebuild, and push. You leave the definition alone. The next submit pulls Thursday's digest. That is the course loop, and the risk is the same loop. A bad Thursday push becomes the next job, because latest moved. Getting Wednesday's bytes back means naming Wednesday's digest, or a tag you treat as immutable. The fast lane is how you learn the pipeline. The audit lane is for the day you have to prove which bytes ran.

The teaching choice is deliberate. latest keeps the lesson short. It does not make the bytes reproducible after the next push.

Next we talk about who is allowed to push that tag from the laptop, and who is allowed to pull it on the GPU instance.
