# PhotoFun
This is a compute platform to transform ancient Chinese art styles into photos, leveraging deep learning technology. It has two parts: web portal and compute backend.

### Web Portal
A Python Flask website for users to upload photos and choose art style type to merge into their photos.

### Compute Backend
A stateless distribued compute system. Master role manages job states with azure table(NoSQL store) as persistent storage. Worker roles perform the photo transformation job based on pre-trained tensorflow model(VGG-16).
