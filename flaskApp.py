from flask import Flask, render_template, request, redirect
import os

import sys

from flask_frozen import Freezer

template_directory = os.getcwd()
navigation_sections = ['Home', 'Projects', 'About', 'Contact']

noProjectDescriptionDefaultMessage = "No description available"

projectShowcaseFolder = "media/showcase/"
projectFolder = "static/projects/"

projectDescriptionFile = "project.oneliner"

buildFolder = "docs"

app = Flask(__name__, template_folder=template_directory)
app.config['FREEZER_DESTINATION'] = buildFolder

#app.config['STATIC_FOLDER'] = template_directory


freezer = Freezer(app)

pageHideHeaders = False

@app.route("/")
@app.route("/index")
@app.route("/index.html")
def home():

	projectsHTML=projectsNoNav()

	return render_template('index.html', navigation=navigation_sections, crumb="home", mimetype='text/html', testHTML=projectsHTML)

@app.route("/projects.html")
def projects():

	allProjects = []

	allDescriptors = {}

	mediaPool = {}


	try:

		for projectName in os.listdir(projectFolder): 

			if  (not projectName.startswith('.') and not projectName.startswith('_')): #Don't put hidden folders.

				allProjects.append(projectName)

				try:
					with open(projectFolder + projectName + '/' + projectDescriptionFile) as f:
						
						if not f:
							continue;
						
						for line in f:
							#print(line, file=sys.stdout)
							#(k, v) = line.split("=")
							allDescriptors[projectName] = line

						#print(f, file=sys.stdout)

				except OSError as e:
					allDescriptors[projectName] = noProjectDescriptionDefaultMessage


				try: #need seperate phases here otherwise I'd wrap into one try / except
					if len(os.listdir(projectFolder + projectName + '/' + projectShowcaseFolder)) > 0: 

						mediaPoolForThisProject = []

						for imageName in os.listdir(projectFolder + projectName + '/' + projectShowcaseFolder):
							if (not imageName.startswith('.') and not imageName.startswith('_')):
								mediaPoolForThisProject.append(projectFolder + projectName + '/' + projectShowcaseFolder + imageName)
								#print(imageName + " added to pool for " + projectName)

						#for x in mediaPoolForThisProject:
							#print(x, file=sys.stdout)	
						#mediaPool[projectName] = os.listdir('static/publicProjects/' + projectName + '/' + 'media/')

						mediaPool[projectName] = mediaPoolForThisProject

					else:
						mediaPool[projectName] = ""
						#print("No media files to showcase for '" + projectName + "'")

				except OSError as e:
					mediaPool[projectName] = ""
					#print(e, file=sys.stdout)
			else:
				continue
	except:
		pass

	return render_template('projects.html', navigation=navigation_sections, crumb="projects", mimetype='text/html', availableProjects=sorted(allProjects), descriptors=allDescriptors, mediaPool=mediaPool, hideNav=False)
	

def getProjectMediaDescriptions():

	allProjects = []

	allDescriptors = {}

	mediaPool = {}


	try:

		for projectName in os.listdir(projectFolder): 

			if  (not projectName.startswith('.') and not projectName.startswith('_')): #Don't put hidden folders.

				allProjects.append(projectName)

				try:
					with open(projectFolder + projectName + '/' + projectDescriptionFile) as f:
						
						if not f:
							continue;
						
						for line in f:
							#print(line, file=sys.stdout)
							#(k, v) = line.split("=")
							allDescriptors[projectName] = line

						#print(f, file=sys.stdout)

				except OSError as e:
					allDescriptors[projectName] = noProjectDescriptionDefaultMessage


				try: #need seperate phases here otherwise I'd wrap into one try / except
					if len(os.listdir(projectFolder + projectName + '/' + projectShowcaseFolder)) > 0: 

						mediaPoolForThisProject = []

						for imageName in os.listdir(projectFolder + projectName + '/' + projectShowcaseFolder):
							if (not imageName.startswith('.') and not imageName.startswith('_')):
								mediaPoolForThisProject.append(projectFolder + projectName + '/' + projectShowcaseFolder + imageName)
								#print(imageName + " added to pool for " + projectName)

						#for x in mediaPoolForThisProject:
							#print(x, file=sys.stdout)	
						#mediaPool[projectName] = os.listdir('static/publicProjects/' + projectName + '/' + 'media/')

						mediaPool[projectName] = mediaPoolForThisProject

					else:
						mediaPool[projectName] = ""
						#print("No media files to showcase for '" + projectName + "'")

				except OSError as e:
					mediaPool[projectName] = ""
					#print(e, file=sys.stdout)
			else:
				continue
	except:
		pass

	return [allProjects, allDescriptors, mediaPool]

def projectsNoNav():
		
		PACKAGED_INFO = getProjectMediaDescriptions()

		return render_template('projects.html', navigation=navigation_sections, crumb="projects", mimetype='text/html', availableProjects=sorted(PACKAGED_INFO[0]), descriptors=PACKAGED_INFO[1], mediaPool=PACKAGED_INFO[2], hideNav=True)
	

@app.route("/projects/<path:subpath>/")
def show_project(subpath):
	# show the subpath after /path/

    return render_template('projects.html', navigation=navigation_sections, crumb="projects", mimetype='text/html', hideNav=False)

@app.route("/about.html")
def about():
	
	return render_template('about.html', navigation=navigation_sections, crumb="about", mimetype='text/html', hideNav=False)

@app.route("/contact.html")
def contact():
	
	return render_template('about.html', navigation=navigation_sections, crumb="contact", mimetype='text/html', hideNav=False)

freezer.freeze()

if __name__ == '__main__':
	freezer.freeze()