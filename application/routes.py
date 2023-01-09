from datetime import datetime

from flask import render_template, request
from flask_paginate import Pagination, get_page_parameter

from application import app
from application import db


@app.route("/")
def get_view_test():
    testviews = list(db.viewTest.find())
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    offset = (page - 1) * per_page
    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(testviews), record_name='testviews')
    views = []
    for testview in db.viewTest.find().skip(offset).limit(per_page):
        testview["_id"] = str(testview["_id"])
        views.append(testview)
    return render_template("view_test.html", testviews=views, pagination=pagination)


@app.route("/shard_test")
def get_shard_test():
    testshards = list(db.testshard.find())
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    offset = (page - 1) * per_page
    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(testshards), record_name='testviews')
    shards = []
    for testshard in db.testshard.find().skip(offset).limit(per_page):
        testshard["_id"] = str(testshard["_id"])
        shards.append(testshard)
    return render_template("shard_test.html", testshards=shards, pagination=pagination)


@app.route("/indexing_test")
def get_indexing_test():
    testindexings = list(db.testindexing.find())
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    offset = (page - 1) * per_page
    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(testindexings),
                            record_name='testviews')
    indexings = []
    for testindexing in db.testindexing.find().skip(offset).limit(per_page):
        testindexing["_id"] = str(testindexing["_id"])
        indexings.append(testindexing)
    return render_template("index_test.html", testindexings=indexings, pagination=pagination)


@app.route("/statics")
def get_statics():
    viewstart = datetime.now()
    viewData = db.viewTest.find({"number": {"$lte": 9304489}})
    viewCount = len(list(viewData))
    viewend = datetime.now()
    resViewTime = (viewend - viewstart).total_seconds() * 1000

    shardstart = datetime.now()
    shardData = db.testshard.find({"number": {"$lte": 9304489}})
    shardCount = len(list(shardData))
    shardend = datetime.now()
    resShardTime = (shardend - shardstart).total_seconds() * 1000

    indexingstart = datetime.now()
    indexingData = db.testindexing.find({"number": {"$lte": 9304489}})
    indexingCount = len(list(indexingData))
    indexingend = datetime.now()
    resIndexingTime = (indexingend - indexingstart).total_seconds() * 1000

    return render_template("statics.html", viewTime=resViewTime, shardTime=resShardTime, indexingTime=resIndexingTime)
