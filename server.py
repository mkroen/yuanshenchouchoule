if __name__ == "__main__":
    from app.blueprints import *
    # NOTE: 使用 ElasticAPM 时如果 debug 是 True 会出现无法上报的问题
    app.run(host="0.0.0.0", port=4000)