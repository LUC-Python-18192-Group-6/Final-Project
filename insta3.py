import imageio
imageio.plugins.ffmpeg.download()

from InstagramAPI import InstagramAPI
username="sebassert"
InstagramAPI = InstagramAPI(username, "SKYLGE")
InstagramAPI.login()

InstagramAPI.getProfileData()
result = InstagramAPI.LastJson
print(result)

print(result['status'])
print(result['user']['full_name'])

InstagramAPI.timelineFeed()

InstagramAPI.getSelfUsernameInfo()
