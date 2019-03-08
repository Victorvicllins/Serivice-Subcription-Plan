Model Archetecture planning
######## PAYSTACK #########
secret key ===== sk_test_8716822981dfee63698a196a1493739637bf403c
public key ===== pk_test_940296bdce25f8f8f03738b18052c5727bd0ce6a

Account
	-email
	-name
	-password

UserProfile
	-user 			(AUTH_USER_MODEL)
	-full name
	-country
	-city
	-phone
	-trainer		(default=False)
	-timestamp

Membership
	-slug
	-type (free, pro, enterprise)
	-price 
	-paystack plan id

UserMembership
	-user    			(AUTH_USER_MODEL)
	-stripe customer id
	-membership type	(foreignkey to Membership)

Subscription
	-user membership 			(foreignkey to UserMembership)
	-stripe subscription id  
	-active

Course
	-title
	-slug
	-description
	-resource url           (Github repo for every course)
	-allowed memberships

Lesson
	-title
	-slug
	-course
	-position
	-video
	-thumbnail

