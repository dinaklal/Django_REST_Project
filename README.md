# Django_REST_Project
Django REST API project 

Hosted in : http://ec2-3-230-56-254.compute-1.amazonaws.com/api/ (http://3.230.56.254/api/ )


Get Users List - 	http://3.230.56.254/api/profile/	GET	List of Users	Without Token

SignUp for the service - 	http://3.230.56.254/api/profile/	POST	Added User	Without Token

Get Films List - 	http://3.230.56.254/api/	GET	List of Films	Without Token

Create Film	- http://3.230.56.254/api/	POST	Created Film	Only With Token

Set favourite genre - 	http://3.230.56.254/api/profile/	PUT	Updated response	Only With Token

Get Reccommended Movies -	http://3.230.56.254/api/profile/recom_movies/	GET	List of Films with same genre	Only With Token

Get Top rated Movies	 - http://3.230.56.254/api//top_rated	GET	List of top upvoted films-first 2	Without Token

Get Single Film - 	http://3.230.56.254/api/1/	GET	All Details of given film	Without Token

Up vote a Movie	- http://3.230.56.254/api/1/upvote	PUT	Increase Upvote count of particular film	Only With Token

Down vote a Movie	- http://3.230.56.254/api/1/downvote	PUT	Increase downvote count of particular film	Only With Token

Write review on a movie - 	http://3.230.56.254/api/review	POST	A logged in user can add review with a film object	Only With Token
