from flask import Flask, request, redirect, jsonify, Blueprint,make_response
from sqlitedef import sqlitedatabase
from array_to.array_to_table import arrayTotable
from array_to.array_to_graph import arrayTograpg
import sqlite3
import os, json
sqlapp=Flask('sqlapp')

@sqlapp.route('/login',methods=['POST'])
def login():
    username=request.form['username']
    password=request.form['password']
    response = {}
    conn = sqlitedatabase.execute_select('select username,password from login where username=? and password=?',(username,password))
    if len(conn) == 0:
        response = {
            'code': 0
        }
        resj = jsonify(response)
        res = make_response(resj)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        response = {
            'code': 10
        }
        resj = jsonify(response)
        res = make_response(resj)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res


@sqlapp.route('/register',methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    response = {}
    conn = sqlitedatabase.execute_select('select username from login where username=?',
                                         (username))
    if len(conn) == 0:
        try:
            conn = sqlite3.connect('database.sqlite')
            cursor = conn.cursor()
            cursor.execute('insert into login (username,password) values (?,?)',
                           (username, password))
            conn.commit()
            response = {
                'code': 10002
            }
        except sqlite3.Error as err:
            raise err
        finally:
            # Close database connection.
            cursor.close()
            conn.close()
            resj = jsonify(response)
            res = make_response(resj)
            res.headers['Access-Control-Allow-Origin'] = '*'
            return res
    else:
        response = {'code': 10003}
        resj = jsonify(response)
        res = make_response(resj)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res




@sqlapp.route('/selectleaguename',methods=['POST'])
def selectleaguename():
    response={}
    status=200
    name=request.form['CountryName']
    conn = sqlitedatabase.execute_select("select League.name,Country.name from Country,League where Country.id=League.country_id and Country.name like ?", (name+"%",))
    if len(conn)==0:
        response={
            'code':10001
        }
        resj = jsonify(response)
        res = make_response(resj)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        attrhead = ['league name', 'country']
        attr = conn[0]
        attr = list(attr)
        for i in range(1, len(conn)):
           attr[0] = attr[0] + '\n' + conn[i][0]
           attr[1] = attr[1] + '\n' + conn[i][1]
        totable = arrayTotable()
        name = 'League'
        path = totable.totable(attrhead, attr, name)
        response={
            'status':200,
            'code':1,
            'path':path
        }
        resj = jsonify(response)
        res = make_response(resj)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res


@sqlapp.route('/selectteamrough',methods=['POST'])
def selectteamrough():
    name = request.form['TeamName']
    response = {}
    status = 200
    conn = sqlitedatabase.execute_select('select distinct Team.team_long_name from Team,League,Match where Match.league_id=League.id and (Team.team_api_id=Match.home_team_api_id or Team.team_api_id=Match.away_team_api_id) and Team.team_long_name like ?', ("%"+name+"%",))
    if len(conn)==0:
        response={
            'code':10001
        }
        resj = jsonify(response)
        res = make_response(resj)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        response={
            'status':200,
            'code':1,
            'attr':conn
        }
        resj = jsonify(response)
        res = make_response(resj)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@sqlapp.route('/selectteamgraph',methods=['POST'])
def selectteamgraph():
    name = request.form['name']
    response = {}
    status = 200
    conn = sqlitedatabase.execute_select(
        'SELECT Team.team_long_name as teamname, Team_Attributes.date,Team_Attributes.buildUpPlaySpeed,\
        Team_Attributes.buildUpPlayDribbling,Team_Attributes.buildUpPlayPassing,\
        Team_Attributes.chanceCreationCrossing,\
        Team_Attributes.chanceCreationPassing, \
        Team_Attributes.chanceCreationShooting,Team_Attributes.defenceAggression,\
        Team_Attributes.defencePressure,\
        Team_Attributes.defenceTeamWidth\
        from Team_Attributes, Team\
        WHERE\
        Team.team_api_id = Team_Attributes.team_api_id\
        and team_long_name=? order by Team_Attributes.date desc limit 1', (name,))
    if len(conn) == 0:
        response = {
            'code': 10001
        }
        resj = jsonify(response)
        res = make_response(resj)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        attr = [conn[0][2],conn[0][3],conn[0][4],conn[0][5],conn[0][6],conn[0][7],conn[0][8],conn[0][9],conn[0][10]]
        tograph = arrayTograpg()
        path = tograph.tographt(attr, name)
        response = {
            'status': 200,
            'code': 1,
            'path': path
        }
        resj = jsonify(response)
        res = make_response(resj)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res


@sqlapp.route('/selectteamattr',methods=['POST'])
def selectteamtactic():
    name = request.form['name']
    response = {}
    status = 200
    conn = sqlitedatabase.execute_select(
        'SELECT Team.team_long_name as teamname, Team_Attributes.date,\
        Team_Attributes.buildUpPlayDribblingClass,Team_Attributes.buildUpPlayPassingClass,\
        Team_Attributes.buildUpPlayPositioningClass, Team_Attributes.buildUpPlaySpeedClass,\
        Team_Attributes.chanceCreationCrossingClass,\
        Team_Attributes.chanceCreationPassingClass, Team_Attributes.chanceCreationPositioningClass, \
        Team_Attributes.chanceCreationShootingClass,Team_Attributes.defenceAggressionClass,\
        Team_Attributes.defenceDefenderLineClass, Team_Attributes.defencePressureClass,\
        Team_Attributes.defenceTeamWidthClass\
        from Team_Attributes, Team\
        WHERE\
        Team.team_api_id = Team_Attributes.team_api_id\
        and team_long_name=?',
        (name,))
    if len(conn) == 0:
        response = {
            'code': 10001
        }
        resj = jsonify(response)
        res = make_response(resj)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        attrhead = ['team name', 'date','buildUpPlayDribbling','buildUpPlayPassing','buildUpPlayPositioning','buildUpPlaySpeed',
                    'chanceCreationCrossing','chanceCreationPassing','chanceCreationPositioning','chanceCreationShooting',
                    'defenceAggression','defenceDefenderLine','defencePressure','defenceTeamWidth']
        attr = conn[0]
        attr = list(attr)
        for i in range(1, len(conn)):
            attr[0] = attr[0] + '\n' + conn[i][0]
            attr[1] = attr[1] + '\n' + conn[i][1]
            attr[2] = attr[2] + '\n' + conn[i][2]
            attr[3] = attr[3] + '\n' + conn[i][3]
            attr[4] = attr[4] + '\n' + conn[i][4]
            attr[5] = attr[5] + '\n' + conn[i][5]
            attr[6] = attr[6] + '\n' + conn[i][6]
            attr[7] = attr[7] + '\n' + conn[i][7]
            attr[8] = attr[8] + '\n' + conn[i][8]
            attr[9] = attr[9] + '\n' + conn[i][9]
            attr[10] = attr[10] + '\n' + conn[i][10]
            attr[11] = attr[11] + '\n' + conn[i][11]
            attr[12] = attr[12] + '\n' + conn[i][12]
            attr[13] = attr[13] + '\n' + conn[i][13]
        totable = arrayTotable()
        path = totable.totable(attrhead, attr, name)
        response = {
            'status': 200,
            'code': 1,
            'path': path
        }
        resj = jsonify(response)
        res = make_response(resj)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@sqlapp.route('/selectplayerrough',methods=['POST'])
def selectplayerrough():
    name = request.form['PlayerName']
    response = {}
    status = 200
    conn = sqlitedatabase.execute_select(
        'SELECT Player.player_name as name\
        FROM Player,Player_Attributes\
        where Player.player_api_id=Player_Attributes.player_api_id and Player.player_name like ?\
        GROUP by player_name\
        order by Player_Attributes.overall_rating desc', ("%"+name+"%",))
    if len(conn) == 0:
        response = {
            'code': 10001
        }
        resj = jsonify(response)
        res = make_response(resj)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:

        response = {
            'status': 200,
            'code': 1,
            'attr': conn
        }
        resj = jsonify(response)
        res = make_response(resj)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res


@sqlapp.route('/selectplayergraph',methods=['POST'])
def selectplayergraph():
    name = request.form['name']
    response = {}
    status = 200
    conn = sqlitedatabase.execute_select(
        'SELECT Player.player_name as name,\
        Player_Attributes.acceleration,Player_Attributes.sprint_speed,\
        Player_Attributes.agility,Player_Attributes.balance,Player_Attributes.dribbling,\
        Player_Attributes.finishing,Player_Attributes.long_shots,\
        Player_Attributes.short_passing,\
        Player_Attributes.long_passing,\
        Player_Attributes.jumping,Player_Attributes.stamina,Player_Attributes.strength,\
        Player_Attributes.interceptions,\
        Player_Attributes.standing_tackle,Player_Attributes.sliding_tackle,\
        Player_Attributes.gk_diving,Player_Attributes.gk_handling,Player_Attributes.gk_kicking,\
        Player_Attributes.gk_positioning,Player_Attributes.gk_reflexes\
        FROM Player,Player_Attributes\
        where Player.player_api_id=Player_Attributes.player_api_id and Player.player_name=?\
        GROUP by Player.player_name', (name,))
    if len(conn) == 0:
        response = {
            'code': 10001
        }
        resj = jsonify(response)
        res = make_response(resj)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        attr = [(conn[0][1]+conn[0][2])/2,(conn[0][3]+conn[0][4]+conn[0][5])/3,
                (conn[0][6]+conn[0][7])/2,(conn[0][8]+conn[0][9])/2,
                (conn[0][13]+conn[0][14]+conn[0][15])/3,
                (conn[0][10]+conn[0][11]+conn[0][12])/3,conn[0][16],conn[0][17],conn[0][18],conn[0][19],conn[0][20]]
        tograph = arrayTograpg()
        path = tograph.tograph(attr, name)
        response = {
            'status': 200,
            'code': 1,
            'path': path
        }
        resj = jsonify(response)
        res = make_response(resj)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@sqlapp.route('/selectplayerattr',methods=['POST'])
def selectplayerattr():
    name = request.form['name']
    response = {}
    status = 200
    conn = sqlitedatabase.execute_select(
        'SELECT Player.player_name as name,Player.birthday,Player.height,Player.weight,Player_Attributes.overall_rating,\
        Player_Attributes.preferred_foot,Player_Attributes.acceleration,Player_Attributes.sprint_speed,\
        Player_Attributes.agility,Player_Attributes.balance,Player_Attributes.dribbling,Player_Attributes.reactions,\
        Player_Attributes.crossing,Player_Attributes.finishing,Player_Attributes.heading_accuracy,Player_Attributes.long_shots,\
        Player_Attributes.short_passing,Player_Attributes.volleys,Player_Attributes.curve,\
        Player_Attributes.free_kick_accuracy,Player_Attributes.long_passing,Player_Attributes.ball_control,\
        Player_Attributes.shot_power,Player_Attributes.jumping,Player_Attributes.stamina,Player_Attributes.strength,\
        Player_Attributes.aggression,Player_Attributes.interceptions,Player_Attributes.positioning,\
        Player_Attributes.vision,Player_Attributes.penalties,Player_Attributes.marking,\
        Player_Attributes.standing_tackle,Player_Attributes.sliding_tackle,\
        Player_Attributes.gk_diving,Player_Attributes.gk_handling,Player_Attributes.gk_kicking,\
        Player_Attributes.gk_positioning,Player_Attributes.gk_reflexes\
        FROM Player,Player_Attributes\
        where Player.player_api_id=Player_Attributes.player_api_id and Player.player_name=?\
        GROUP by Player.player_name', (name,))
    if len(conn) == 0:
        response = {
            'code': 10001
        }
        return response, status
    else:
        attrhead = ['name', 'birthday','height','weight','overall rating','preferred_foot',
                    'acceleration','sprint_speed','agility','balance','dribbling','reactions',
                    'crossing','finishing','heading_accuracy','long_shots','short_passing',
                    'volleys','curve','free_kick_accuracy','long_passing','ball_control',
                    'shot_power','jumping','stamina','strength','aggression','interceptions',
                    'positioning','vision','penalties','marking',
                    'standing_tackle','sliding_tackle','gk_diving','gk_handling','gk_kicking','gk_positioning',
                    'gk_reflexes']
        attr = conn[0]
        attr = list(attr)
        totable = arrayTotable()
        path = totable.totable(attrhead, attr, name)
        response = {
            'status': 200,
            'code': 1,
            'path': path
        }
        resj = jsonify(response)
        res = make_response(resj)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@sqlapp.route('/selectteammatch',methods=['POST'])
def selectteammatch():
    name = request.form['name']
    response = {}
    status = 200
    conn = sqlitedatabase.execute_select(
        'SELECT T1.team_long_name as teamname,League.name,Match.date,T2.team_long_name as hometeam,Match.home_team_goal,T3.team_long_name as awayteam,Match.away_team_goal \
        from Team T1,Team T2,Team T3,League,Match \
        WHERE Match.league_id=League.id and T2.team_api_id=Match.home_team_api_id AND T3.team_api_id=Match.away_team_api_id \
        AND (T1.team_api_id=Match.home_team_api_id or T1.team_api_id=Match.away_team_api_id) AND T1.team_long_name=? \
        order by Match.date desc limit 10'
        , (name,))
    if len(conn) == 0:
        response = {
            'code': 10001
        }
        return response, status
    else:
        attrhead = ['team_name','league','date','home_team','h_goal','away_team','a_goal']
        attr = conn[0]
        attr = list(attr)
        for i in range(1, len(conn)):
            attr[0] = attr[0] + '\n' + conn[i][0]
            attr[1] = attr[1] + '\n' + conn[i][1]
            attr[2] = attr[2] + '\n' + conn[i][2]
            attr[3] = attr[3] + '\n' + conn[i][3]
            attr[4] = str(attr[4]) + '\n ' + str(conn[i][4])
            attr[5] = attr[5] + '\n' + conn[i][5]
            attr[6] = str(attr[6]) + '\n ' + str(conn[i][6])
        totable = arrayTotable()
        path = totable.totable(attrhead, attr, name)
        response = {
            'status': 200,
            'code': 1,
            'path': path
        }
        resj = jsonify(response)
        res = make_response(resj)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res


if __name__ == '__main__':
    sqlapp.run(debug=True,host='0.0.0.0', port=5000)