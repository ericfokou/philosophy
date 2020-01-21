#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Ne pas se soucier de ces imports
import setpath
from flask import Flask, render_template, session, request, redirect, flash, url_for
from getpage import getPage

app = Flask(__name__)

app.secret_key = "INF344EricKey"

cache = {}


@app.route('/', methods=['GET'])
def index():
	print('---------------------------------------')
	session.pop('article_redirect', None)
	session.pop('initial_article', None)
	session.pop('current_article', None)
	session.pop('score', None)
	return render_template('index.html', message="")

# @app.route('/test')
# def test():
#     return render_template('test.html', message="")

# Si vous définissez de nouvelles routes, faites-le ici

@app.route('/new-game', methods=['POST'])
def new_party():
	# traiter les données reçues
	article = request.form.get('title', 'wikipedia')
	session['initial_article'] = article
	session['current_article'] = article
	session['score'] = 0
	#return redirect(url_for('play_game'))
	return redirect('/game')
	#return render_template('game.html',  message="from new-game")

@app.route('/game', methods=['GET'])
def play_game():
	global cache
	if 'current_article' in session:
		article = session['current_article']
	else:
		return redirect('/')

	if (article in cache.keys()):
		title = article
		aList = cache[article]
		#print('In cache')
	else:
		title,aList = getPage(article)
		cache[title] = aList
		# if (title != article):		# Ne pas faire ceci car Philosophique se retrouvera dans le cache
										# et session['current_article'] pourra contenir ainsi 'Philosophique ' 
		# 		cache[article] = aList
	
	if (session['score'] == 0):
		session['current_article'] = title
		session['article_redirect'] = title

	if (aList == None):
		print('None')
		flash(u'La page demandée n’existe pas.', 'erreur')
		flash(u' Nous vous avons redirigé sur la page d\'acceuil.', 'erreur')
		return render_template('index.html')
	if (len(aList) == 0):
		flash(u'Il n\'existe pas de lien sur la page que vous avez demandée.', 'erreur')
		flash(u' Nous vous avons redirigé sur la page d\'acceuil.', 'erreur')
		return render_template('index.html')
	
	return render_template('game.html',  currentTitle=title, items=aList)

@app.route('/move', methods=['POST'])
def move_link():
	global cache
	
	score_page = int(request.form.get('score', 0))
	linkChoice = request.form.get('linkChoice', "")

	if (score_page != int(session['score'])): # controle sur l'utilisation de plusieurs onglets
		if (linkChoice != session['current_article']):
			flash(u'Attention vous avez déja progressé sur un autre onglet.', 'erreur')
			flash(u'Si vous souhaitez recommencer une nouvelle partie, remplir le formulaire ci-dessous sinon ouvrez la page http://localhost:5000/game pour continuer la partie', 'erreur')
			return render_template('index.html')
		else:
			title = linkChoice
			aList = cache[linkChoice]

	else:
		session['score'] = int(session['score']) + 1
		# controle sur la modification de formulaire avec les outils de developpement
		previous_article = session['current_article']
		if (linkChoice not in cache[previous_article]):
			flash(u'Vous avez essayé de tricher petit MALIN!!!!.', 'erreur')
			flash(u' Réessayez en étant honnète :) .', 'erreur')
			return render_template('game.html',  currentTitle=previous_article, items=cache[previous_article])
		
		if (linkChoice == session['article_redirect']):
			flash(u'BRAVO!!!!  Tous les chemins mènent à '+str(session['article_redirect'])+', votre SCORE:'+str(session['score']), 'succes')
			return render_template('index.html')
		
		#print("linkChoice: "+linkChoice)
		if (linkChoice in cache.keys()):
			title = linkChoice
			aList = cache[linkChoice]
			#print('In cache')
		else:
			title,aList = getPage(linkChoice)
			cache[title] = aList
			if (title != linkChoice):
				cache[linkChoice] = aList
			#print('Not In cache')

		session['current_article'] = title

	#print(aList)
	if (aList == None):
		#print('None')
		flash(u'La page demandée n’existe pas.', 'erreur')
		flash(u' Nous vous avons redirigé sur la page d\'acceuil.', 'erreur')
		return render_template('index.html')
	if (len(aList) == 0):
		flash(u'Il n\'existe pas de lien sur la page que vous avez demandée.', 'erreur')
		flash(u' Nous vous avons redirigé sur la page d\'acceuil.', 'erreur')
		return render_template('index.html')

	return render_template('game.html',  currentTitle=title, items=aList)

@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
def ma_page_erreur(error):
    return "My Error Page {}".format(error), error.code

if __name__ == '__main__':
	app.config['PERMANENT_SESSION_LIFETIME'] = 3600 # la session dure une heure
	app.run(debug=True)

