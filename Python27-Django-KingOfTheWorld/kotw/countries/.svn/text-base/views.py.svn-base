from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from countries.models import Country, Build, Army, Tech, Resource
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from operator import div
from buildings.models import Building
from governments.models import Government, effects
from techs.models import Tech as Techs
from military.models import Military
from decimal import Decimal

title = "King of the World"
css = 'kotw.css'

enterprise_mod=Building.objects.get(type="enterprise").effect_val
industrial_mod=Building.objects.get(type="industrial").effect_val
farm_mod=Building.objects.get(type="farm").effect_val
oil_mod=Building.objects.get(type="oil_rig").effect_val
unused_mod=Building.objects.get(type="unused").effect_val

gov_train_pro=effects.objects.get(effect_name="decrease training costs").effect_val
gov_build_pro=effects.objects.get(effect_name="decrease construction costs").effect_val
gov_build_con=effects.objects.get(effect_name="increase construction costs").effect_val
gov_tech_con=effects.objects.get(effect_name="decrease technology effectiveness").effect_val
gov_tech_pro=effects.objects.get(effect_name="increase technology effectiveness").effect_val

army_tech=Techs.objects.get(type="Military").effect_val

def add(x,y):
	return (x+y)

@login_required()
def explore(request):
	c = Country.objects.get(user=request.user)
	b = Build.objects.get(country=c)
	r = Resource.objects.get(country=c)
	a = Army.objects.get(country=c)
	t = Tech.objects.get(country=c)
	nw = b.unused*20+(b.farm+b.enterprise+b.residence+b.industry+b.army+b.labs+b.oil)*75+r.pop+a.troops*2+a.jets*3+a.turrets*3+a.tanks*8+r.gold*1/1000+r.food*0+(t.military+t.medical+t.economics+t.residential+t.geography+t.weapons)*1/100
	troop_cost = 3+(r.land-300)/(nw/r.land)
	gold_cost = (5*r.land-300)*600/r.land
	food_cost = gold_cost/troop_cost
	costs=(troop_cost, gold_cost, food_cost)
	current=(a.troops, r.gold, r.food)
	target=map(div,current,costs)
	number_of_acres = min(target)
	if request.method=='POST':
		num_acres=request.POST['num_acres']
		troops=int(str(num_acres))*troop_cost
		gold=int(str(num_acres))*gold_cost
		food=int(str(num_acres))*food_cost
		a.troops=a.troops-troops
		r.gold=r.gold-gold
		r.food=r.food-food
		b.unused=b.unused+int(str(num_acres))
		r.land=b.unused+b.farm+b.enterprise+b.residence+b.industry+b.army+b.labs+b.oil
		b.save()
		a.save()
		r.save()
		return HttpResponseRedirect('/kotw/explore/')
	data = {'page_title':title, 'page_css':css}
	data.update(troop_costs=str(troop_cost), gold_costs=str(gold_cost), food_costs=str(food_cost))
	data.update(country_troops=a.troops, country_gold=r.gold, country_food=r.food, country_oil=r.oil, country_pop=r.pop, country_land=r.land, max_acres=number_of_acres)
	return render_to_response('countries/explore.html', data, context_instance=RequestContext(request))

@login_required()
def build(request):
	c = Country.objects.get(user=request.user)
	b = Build.objects.get(country=c)
	r = Resource.objects.get(country=c)
	data = {'page_title':title, 'page_css':css}
	data.update(country_gold=r.gold, country_food=r.food, country_oil=r.oil, country_pop=r.pop, country_land=r.land)
	data.update(farms=b.farm, enterprise=b.enterprise, residences=b.residence, industrial=b.industry, bases=b.army, labs=b.labs, oil_rigs=b.oil, unused=b.unused)
	build_mod=1
	if c.government=='D':
		build_mod=build_mod*gov_build_con
	elif c.government=='T':
		build_mod=build_mod*gov_build_pro
	build_cost=int(((r.land+1500)*2/7)*build_mod)
	max_build=min(r.gold/build_cost, b.unused)
	data.update(building_cost=build_cost, max_buildings=max_build)
	msg=""
	if request.method=='POST':
		build_query=request.POST.getlist('build')
		build_tar=map(int,build_query)
		sum_build=sum(build_tar)
		if sum_build>max_build:
			msg="You do not have enough resources to build " + str(sum_build) + " acres."
			data.update(msgs=msg)
		else:
			if sum_build<=b.unused:
				b.unused=b.unused-sum_build
				b.farm=b.farm+build_tar[0]
				b.enterprise=b.enterprise+build_tar[1]
				b.residence=b.residence+build_tar[2]
				b.industry=b.industry+build_tar[3]
				b.army=b.army+build_tar[4]
				b.labs=b.labs+build_tar[5]
				b.oil=b.oil+build_tar[6]
				r.gold=r.gold-(sum_build*build_cost)
				b.save()
				r.save()
				return HttpResponseRedirect('/kotw/build/')
			else:
				msg.append("Can't build more structures than the number of unused acres.")
				data.update(msgs=msg)
	return render_to_response('countries/build.html', data, context_instance=RequestContext(request))

@login_required
def military(request):
	c = Country.objects.get(user=request.user)
	b = Build.objects.get(country=c)
	r = Resource.objects.get(country=c)
	a = Army.objects.get(country=c)
	t = Tech.objects.get(country=c)
	troop = Military.objects.get(unit="Troops")
	jet = Military.objects.get(unit="Jets")
	turret = Military.objects.get(unit="Turrets")
	tank = Military.objects.get(unit="Tanks")
	data = {'page_title':title, 'page_css':css}
	data.update(country_gold=r.gold, country_food=r.food, country_oil=r.oil, country_pop=r.pop, country_land=r.land)
	train_mod=1
	build_train_mod=(1-b.industry/r.land*industrial_mod)
	train_tech_mod=1-((t.military/r.land)/100*army_tech)
	if c.government=='C':
		train_mod=train_mod*gov_train_pro
	elif c.government=='T':
		train_tech_mod=1+(1-train_tech_mod)*gov_tech_con
	elif c.government=='DE':
		train_tech_mod=train_tech_mod*gov_tech_pro
	train_mod=train_mod * build_train_mod * train_tech_mod

	troop_cost=int(350*train_mod)
	jet_cost=int(500*train_mod)
	turret_cost=int(500*train_mod)
	tank_cost=int(1000*train_mod)

	max_troop=min(r.pop, r.gold/troop_cost)
	max_jet=min(a.troops/2, r.gold/jet_cost)
	max_turret=min(a.troops/2, r.gold/turret_cost)
	max_tank=min(a.troops/4, r.gold/tank_cost)

	data.update(troops_off=troop.offense, troops_def=troop.defense, cur_troops=a.troops, troops_cost=troop_cost, max_troops=max_troop)
	data.update(jets_off=jet.offense, jets_def=jet.defense, cur_jets=a.jets, jets_cost=jet_cost, max_jets=max_jet)
	data.update(turrets_off=turret.offense, turrets_def=turret.defense, cur_turrets=a.turrets, turrets_cost=turret_cost, max_turrets=max_turret)
	data.update(tanks_off=tank.offense, tanks_def=tank.defense, cur_tanks=a.tanks, tanks_cost=tank_cost, max_tanks=max_tank)
	msg=""
	data.update(msgs=msg)
	if request.method=='POST':
		train_query=request.POST.getlist('train')
		train_army=map(int,train_query)
		errors=0
		sum_training_costs=(train_army[0]*troop_cost)+(train_army[1]*jet_cost)+(train_army[2]*turret_cost)+(train_army[3]*tank_cost)
		if sum_training_costs>r.gold:
			msg=msg+("Not enough resources to complete your order.")
			data.update(msgs=msg)
			return render_to_response('countries/military.html', data, context_instance=RequestContext(request))

		if train_army[0]>max_troop:
			msg=msg+("Not enough resources to train " + str(train_army[0]) + " Troops.\n")
			errors=errors+1
		else:
			r.gold=r.gold-(train_army[0]*troop_cost)
			r.pop=r.pop-train_army[0]
			a.troops=a.troops+train_army[0]
			r.save()
			a.save()

		if train_army[1]>max_jet:
			msg=msg+("Not enough reources to train " + str(train_army[1]) + " Jets\n")
			errors=errors+1
		else:
			r.gold=r.gold-(train_army[1]*jet_cost)
			a.troops=a.troops-(train_army[1]*2)
			a.jets=a.jets+train_army[1]
			r.save()
			a.save()

		if train_army[2]>max_turret:
			msg=msg+("Not enough reources to train " + str(train_army[2]) + " Turrets\n")
			errors=errors+1
		else:
			r.gold=r.gold-(train_army[2]*turret_cost)
			a.troops=a.troops-(train_army[2]*2)
			a.turrets=a.turrets+train_army[2]
			r.save()
			a.save()

		if train_army[3]>max_turret:
			msg=msg+("Not enough reources to train " + str(train_army[3]) + " Tanks\n")
			errors=errors+1
		else:
			r.gold=r.gold-(train_army[3]*tank_cost)
			a.troops=a.troops-(train_army[3]*4)
			a.tanks=a.tanks+train_army[3]
			r.save()
			a.save()

		if errors==0:
			return HttpResponseRedirect('/kotw/military/')
		else:
			data.update(msgs=msg)
	return render_to_response('countries/military.html', data, context_instance=RequestContext(request))

def research(request):
	c = Country.objects.get(user=request.user)
	b = Build.objects.get(country=c)
	r = Resource.objects.get(country=c)
	a = Army.objects.get(country=c)
	t = Tech.objects.get(country=c)
	data = {'page_title':title, 'page_css':css}
	data.update(country_gold=r.gold, country_food=r.food, country_oil=r.oil, country_pop=r.pop, country_land=r.land)
	data.update(military=t.military, medical=t.medical, economics=t.economics, residential=t.residential, geography=t.geography, weapons=t.weapons)
	curTech=[]
	tech_vals=[0,0,0,0,0,0]
	tech_vals[0]=Techs.objects.get(type="Military")
	tech_vals[1]=Techs.objects.get(type="Medical")
	tech_vals[2]=Techs.objects.get(type="Economics")
	tech_vals[3]=Techs.objects.get(type="Residential")
	tech_vals[4]=Techs.objects.get(type="Geography")
	tech_vals[5]=Techs.objects.get(type="Weapons")
	curTech.append((float(t.military)/float(r.land))/100.0*float(tech_vals[0].effect_val))
	curTech.append((float(t.medical)/float(r.land))/100.0*float(tech_vals[1].effect_val))
	curTech.append((float(t.economics)/float(r.land))/100.0*float(tech_vals[2].effect_val))
	curTech.append((float(t.residential)/float(r.land))/100.0*float(tech_vals[3].effect_val))
	curTech.append((float(t.geography)/float(r.land))/100.0*float(tech_vals[4].effect_val))
	curTech.append((float(t.weapons)/float(r.land))/100.0*float(tech_vals[5].effect_val))
	if c.government=='T':
		gov_mod=gov_tech_con
		for ct in curTech:
			ct=ct*float(gov_mod)
	elif c.government=='DE':
		gov_mod=gov_tech_pro
		for ct in curTech:
			ct=ct*float(gov_mod)
	curTech=map(float,curTech)
	curTech=[round(x,2) for x in curTech]
	for i in range(len(curTech)):
		curTech[i] = str(tech_vals[i].effect_name)+" by "+str(curTech[i]*100)+"%"
	data.update(military_effect=curTech[0], medical_effect=curTech[1], economics_effect=curTech[2], residential_effect=curTech[3], geography_effect=curTech[4], weapons_effect=curTech[5])
	max_military=(r.land*100)-t.military
	max_medical=(r.land*100)-t.medical
	max_economics=(r.land*100)-t.economics
	max_residential=(r.land*100)-t.residential
	max_geography=(r.land*100)-t.geography
	max_weapons=(r.land*100)-t.weapons
	res_costs=(t.military+t.medical+t.economics+t.residential+t.geography+t.weapons)*5/18
	max_tech=r.gold/res_costs
	data.update(max_mil=min(max_military,max_tech), max_med=min(max_medical,max_tech), max_econ=min(max_economics,max_tech), max_res=min(max_residential,max_tech), max_geo=min(max_geography,max_tech), max_weap=min(max_weapons,max_tech))
	data.update(cpp=res_costs, max_techs=max_tech)
	msgs=""
	if request.method=='POST':
		tech_query=request.POST.getlist('techs')
		resList=map(int,tech_query)
		sum_research=sum(resList)
		if sum_research>max_tech:
			msg="You do not have enough resources to research " + str(sum_research) + " points of tech."
			data.update(msgs=msg)
		else:
			r.gold=r.gold-(sum_research*res_costs)
			t.military=t.military+resList[0]
			t.medical=t.medical+resList[1]
			t.economics=t.economics+resList[2]
			t.residential=t.residential+resList[3]
			t.geography=t.geography+resList[4]
			t.weapons=t.weapons+resList[5]
			r.save()
			t.save()
			return HttpResponseRedirect('/kotw/research/')
	return render_to_response('countries/research.html', data, context_instance=RequestContext(request))
