#####################################################

# routes module

# responsible for defining how the application
# should handle different URL requests
#####################################################

from datetime import datetime

from flask import render_template, request
from flask_paginate import Pagination, get_page_parameter

from application import app
from application import db


@app.route("/")
def get_view_test():
    """
    page for displaying data in View mode
    """
    # retrieve all the entries in the 'viewTest' collection of the database
    testviews = list(db.viewTest.find())
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # paginate the results for easy navigation.
    per_page = 10
    offset = (page - 1) * per_page
    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(testviews), record_name='testviews')
    views = []
    # convert the _id field of each viewtest object from ObjectId to string to be handled by frontend easily
    for testview in db.viewTest.find().skip(offset).limit(per_page):
        testview["_id"] = str(testview["_id"])
        views.append(testview)
    # return the template
    # along with the paginated data
    # and pagination object to be displayed on the webpage.
    return render_template("view_test.html", testviews=views, pagination=pagination)

@app.route("/shard_test")
def get_shard_test():
    """
    page for displaying data in shard mode
    """
    # retrieve all the entries in the 'testshard' collection of the database
    testshards = list(db.testshard.find())
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # paginate the results for easy navigation.
    per_page = 10
    offset = (page - 1) * per_page
    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(testshards), record_name='testviews')
    shards = []
    # convert the _id field of each testshard object from ObjectId to string to be handled by frontend easily
    for testshard in db.testshard.find().skip(offset).limit(per_page):
        testshard["_id"] = str(testshard["_id"])
        shards.append(testshard)
    # return the template
    # along with the paginated data
    # and pagination object to be displayed on the webpage.
    return render_template("shard_test.html", testshards=shards, pagination=pagination)


@app.route("/indexing_test")
def get_indexing_test():
    """
    page for displaying data in indexing mode
    """
    # retrieve all the entries in the 'testindexing' collection of the database
    testindexings = list(db.testindexing.find())
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # paginate the results for easy navigation.
    per_page = 10
    offset = (page - 1) * per_page
    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(testindexings),
                            record_name='testviews')
    indexings = []
    # convert the _id field of each testshard object from ObjectId to string to be handled by frontend easily
    for testindexing in db.testindexing.find().skip(offset).limit(per_page):
        testindexing["_id"] = str(testindexing["_id"])
        indexings.append(testindexing)
    # return the template
    # along with the paginated data
    # and pagination object to be displayed on the webpage.
    return render_template("index_test.html", testindexings=indexings, pagination=pagination)


@app.route("/comparation")
def get_comparation():
    """
    This function serves as the endpoint for comparing the performance of different ways of querying data.
    Specifically, it compares the time it takes to retrieve data from the 'viewTest' collection,
    the 'testshard' collection, and the 'testindexing' collection.
    """

    # use the 'datetime' module to record the start and end time of each query,
    # then calculates the duration of each query and stores them in the variables
    # 'resViewTime', 'resShardTime', and 'resIndexingTime'.

    # $lte operator is used for filtering data and 9304489 is used as value for number field,
    # we search for this ID each time for searchung

    # count time for views
    viewstart = datetime.now()
    viewData = db.viewTest.find({"number": {"$lte": 9304489}})
    viewCount = len(list(viewData))
    viewend = datetime.now()
    resViewTime = (viewend - viewstart).total_seconds() * 1000

    # count time for sharding
    shardstart = datetime.now()
    shardData = db.testshard.find({"number": {"$lte": 9304489}})
    shardCount = len(list(shardData))
    shardend = datetime.now()
    resShardTime = (shardend - shardstart).total_seconds() * 1000

    # count time for indexing
    indexingstart = datetime.now()
    indexingData = db.testindexing.find({"number": {"$lte": 9304489}})
    indexingCount = len(list(indexingData))
    indexingend = datetime.now()
    resIndexingTime = (indexingend - indexingstart).total_seconds() * 1000

    # use the render_template function to return the 'comparation.html' template
    # along with the calculated time taken by different query methods,
    # this time duration are useful for analyzing the performance of the different querying methods.
    return render_template("comparation.html", viewTime=resViewTime, shardTime=resShardTime, indexingTime=resIndexingTime)
