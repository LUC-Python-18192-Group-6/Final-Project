import imageio
imageio.plugins.ffmpeg.download()

from InstagramAPI import InstagramAPI
username="sebassert"
InstagramAPI = InstagramAPI(username, "SKYLGE")
InstagramAPI.login()

InstagramAPI.getProfileData()
result = InstagramAPI.LastJson
print(result)

print(result['user']['profile_pic_url'])
print(result['user']['full_name'])

print(InstagramAPI.timelineFeed())

print(InstagramAPI.getSelfUsernameInfo())
