#!/usr/bin/env bash
# using puppet to make changes

file {'ect/ssh/ssh_cofig;:
	ensure => present,

content =>"

	#SSH client configuration
	host
	identityfile ~/.ssh/school
	passwordAuthentication no
	",
}
