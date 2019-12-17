from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.urls import reverse
# Create your views here.
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Categories, News, SalesSentences
from .models_gfl import Informations, Sentences, SalestalkReports, UserBrowseHistories
from django.db import connection
import json

def index(request):
	
	listTopNews = News.objects.filter(category__category='topside-news')
	#SELECT * FROM tsukapota_news join tsukapota_categories on tsukapota_news.category_id = tsukapota_categories.id WHERE tsukapota_categories.category = 'topside-news'  
	listBottomNews = News.objects.filter(category__category='bottomside-news')
	listLeftNews = News.objects.filter(category__category='leftside-news')
	listRightNews = News.objects.filter(category__category='rightside-news')

	cursor = connection.cursor()
	cursor.execute("SELECT informations.id, informations.train_subway_station_1, TRUNCATE(informations.price_1 /10000, 0), informations.floor_plan, informations.property_category, REPLACE(REPLACE(sentences.sentence_content, '<span>', ''), '</span>', '') FROM `gfl-testgfl`.informations left join `gfl-testgfl`.sentences on sentences.property_no = informations.property_id WHERE informations.property_id = (SELECT property_no FROM (SELECT * FROM `gfl-testgfl`.user_browse_histories ORDER BY user_browse_histories.created_at desc limit 10) as A ORDER BY stay_time desc limit 1) and sentences.factor_code > 16 and sentences.sentence_id in  ('v2_s12', 'v2_s22', 'v2_s32') order by RAND() limit 1;")
	salesSentences = cursor.fetchall()[0]
	print(salesSentences)

	# cursor = connection.cursor()
	cursor.execute("SELECT REPLACE(REPLACE(salestalk, '<span>', ''), '</span>', '') FROM `gfl-testgfl`.`salestalk_reports` WHERE common_property_no=(SELECT `common_property_no` from `gfl-testgfl`.informations WHERE property_id =  (SELECT `property_no` FROM (SELECT * FROM `gfl-testgfl`.user_browse_histories ORDER BY user_browse_histories.created_at desc limit 10) as A ORDER BY stay_time desc limit 1)) and case_conditions LIKE CONCAT('%', (select  max(case when rank=1 then name end) as `highest value` from (select  common_property_no, @rownum := @rownum + 1 AS rank, name, amt from (select common_property_no, age as amt, 'age' as name from `gfl-testgfl`.charts where property_no = (SELECT property_no FROM (SELECT * FROM `gfl-testgfl`.user_browse_histories ORDER BY user_browse_histories.created_at desc limit 10) as A ORDER BY stay_time desc limit 1) union select common_property_no, closeness, 'closeness' from `gfl-testgfl`.charts where property_no = (SELECT property_no FROM (SELECT * FROM `gfl-testgfl`.user_browse_histories ORDER BY user_browse_histories.created_at desc limit 10) as A ORDER BY stay_time desc limit 1) union select common_property_no, size, 'size' from `gfl-testgfl`.charts where property_no = (SELECT property_no FROM (SELECT * FROM `gfl-testgfl`.user_browse_histories ORDER BY user_browse_histories.created_at desc limit 10) as A ORDER BY stay_time desc limit 1) union select common_property_no, convenient, 'convenient' from `gfl-testgfl`.charts where property_no = (SELECT property_no FROM (SELECT * FROM `gfl-testgfl`.user_browse_histories ORDER BY user_browse_histories.created_at desc limit 10) as A ORDER BY stay_time desc limit 1) union select common_property_no, security, 'security' from `gfl-testgfl`.charts where property_no = (SELECT property_no FROM (SELECT * FROM `gfl-testgfl`.user_browse_histories ORDER BY user_browse_histories.created_at desc limit 10) as A ORDER BY stay_time desc limit 1) union select common_property_no, comfortable, 'comfortable' from `gfl-testgfl`.charts where property_no = (SELECT property_no FROM (SELECT * FROM `gfl-testgfl`.user_browse_histories ORDER BY user_browse_histories.created_at desc limit 10) as A ORDER BY stay_time desc limit 1) ) amounts, (SELECT @rownum :=0) r order by amt desc limit 2 ) top2 group by common_property_no), '%') limit 5")
	salesComment1 = cursor.fetchall()
	print(salesComment1)

	cursor.execute("SELECT REPLACE(REPLACE(salestalk, '<span>', ''), '</span>', '') FROM `gfl-testgfl`.`salestalk_reports` WHERE common_property_no=(SELECT `common_property_no` from `gfl-testgfl`.informations WHERE property_id =  (SELECT `property_no` FROM (SELECT * FROM `gfl-testgfl`.user_browse_histories ORDER BY user_browse_histories.created_at desc limit 10) as A ORDER BY stay_time desc limit 1)) and case_conditions LIKE CONCAT('%', (select  max(case when rank=2 then name end) as `second value` from (select  common_property_no, @rownum := @rownum + 1 AS rank, name, amt from (select common_property_no, age as amt, 'age' as name from `gfl-testgfl`.charts where property_no = (SELECT property_no FROM (SELECT * FROM `gfl-testgfl`.user_browse_histories ORDER BY user_browse_histories.created_at desc limit 10) as A ORDER BY stay_time desc limit 1) union select common_property_no, closeness, 'closeness' from `gfl-testgfl`.charts where property_no = (SELECT property_no FROM (SELECT * FROM `gfl-testgfl`.user_browse_histories ORDER BY user_browse_histories.created_at desc limit 10) as A ORDER BY stay_time desc limit 1) union select common_property_no, size, 'size' from `gfl-testgfl`.charts where property_no = (SELECT property_no FROM (SELECT * FROM `gfl-testgfl`.user_browse_histories ORDER BY user_browse_histories.created_at desc limit 10) as A ORDER BY stay_time desc limit 1) union select common_property_no, convenient, 'convenient' from `gfl-testgfl`.charts where property_no = (SELECT property_no FROM (SELECT * FROM `gfl-testgfl`.user_browse_histories ORDER BY user_browse_histories.created_at desc limit 10) as A ORDER BY stay_time desc limit 1) union select common_property_no, security, 'security' from `gfl-testgfl`.charts where property_no = (SELECT property_no FROM (SELECT * FROM `gfl-testgfl`.user_browse_histories ORDER BY user_browse_histories.created_at desc limit 10) as A ORDER BY stay_time desc limit 1) union select common_property_no, comfortable, 'comfortable' from `gfl-testgfl`.charts where property_no = (SELECT property_no FROM (SELECT * FROM `gfl-testgfl`.user_browse_histories ORDER BY user_browse_histories.created_at desc limit 10) as A ORDER BY stay_time desc limit 1) ) amounts, (SELECT @rownum :=0) r order by amt desc limit 2 ) top2 group by common_property_no), '%') limit 5")
	salesComment2 = cursor.fetchall()
	print(salesComment2)

	# js_data = simplejson.dumps(my_dict)

	context = {
		'listTopNews': listTopNews,
		'listBottomNews': listBottomNews,
		'listLeftNews': listLeftNews,
		'listRightNews': listRightNews,
		'salesSentences': salesSentences,
		'salesComment1': salesComment1,
		'salesComment2': salesComment2,
	}
	return render(request, 'tsukapota/index-pc.html', context)


 # SELECT informations.train_subway_station_1, informations.price_1 /10000, informations.floor_plan, informations.property_category, sentences.sentence_content  
 # FROM `gfl-testgfl`.informations left join
 # `gfl-testgfl`.sentences on sentences.property_no = informations.property_id
 # WHERE 
 #     informations.property_id = (SELECT property_no FROM (SELECT * FROM `gfl-testgfl`.user_browse_histories ORDER BY user_browse_histories.created_at desc limit 10) as A ORDER BY stay_time desc limit 1) 
 #     and sentences.factor_code > 16 
 #     and sentences.sentence_id in  ('v2_s12', 'v2_s22', 'v2_s32') order by RAND() limit 1;