- post thumbnail deletion, using a cron job and a python script
- user profile pic api endpoint and imagekit conversion

>>>>>>>>>>>>>>>>>>>>>
- do blocked user thingy
- blocked users cannot see media/post photos too
>>>>>>>>>>>>>>>>>>>>>

- simplify things like
```py
if (request.method in ("PUT", "PATCH")) and (self.kwargs["username"] != request.user.username):
```
by using api/users/self
rather than api/users/ajitid and using the above condition as then they will be simplified to
just read requests
^ this is still debatable as this doesn't solves deleting comment or posts plus we are breaking consistency for just one case


- https://github.com/MatteoGabriele/vue-progressive-image
- all about profile and post image
- reset pwd flow and activate account email
- iframe share
- failsafe - following themself
- profile edit
- search and explore
- bookmark posts - save reference
- @ tagging and # hashtag
- block and private and failsafe for block
- cloudfare, cloudinary, psql











- [ ] nametag
- [ ] change default svg profile pic back to insta black
- [ ] filtering | query param
- [ ] csrf, DRF loggin in only of user is staff
- [ ] auth everywhere
- [ ] post photo change from a different url, same for email
- [ ] create profile model, UserView, follow count
- [ ] add authorisation classes for blocked and private account
- [ ] stripping values like username and name b4 saving... does dj models does it for you??
- [ ] validation classes drf
- [ ] google signup
- [ ] if user not active don't show posts and all
- [ ] /api/users/ajitid should contain profile info or be in router
- [ ] notifications (django notifications??)
- [ ] profile -> private, disabled
- [ ] a user cannot be its own follower or following or blocked check
- [ ] prpgressive image loading
- [ ] 1080-post_photo 320-post_thumb 240-dp
- [ ] canvas - zoom in, zoom out, rotate, white bg (customizable maybe) if out of square, filter b4 filling with white
- [ ] default fit ot square 30% above image size
- [ ] drf only allow specific image size
- [ ] https://html.com/attributes/img-srcset/
- [ ] remove image on post and profile delete except default.jpg for profile
- [ ] forgot password flow
- [ ] liking, commenting on own post
- [ ] don't notify on liking, commenting on own post, also customizable notify settings
- [ ] password reset and suer registration w/o stripping password
- [ ] django restart - a dev package - delete migrations, pycache, make migrations and migrate and create superuser
- [ ] graphql/graphene?? :shrug:
- [ ] search
- [ ] chat
- [ ] django fakery or just faker with bulk create
- [ ] polaroid filters - frontend
