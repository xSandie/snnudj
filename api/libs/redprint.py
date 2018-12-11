class Redprint:#因为蓝图是针对模块的，而非针对视图函数
    def __init__(self,name):#传入名字，构造reprint对象
        self.name=name
        self.mound=[]

    def route(self, rule, **options):#实现api的route装饰器方法,rule即url，option即方法
        def decorator(f):#f是装饰器作用的方法
            self.mound.append((f,rule,options))#先保存成一个一个的元组，不着急注册
            return f

        return decorator
    pass

    def register(self,bp,url_prefix=None):#bp即传入的蓝图对象，为了调用add_url_rule方法
        if url_prefix is None:
            url_prefix='/'+self.name
        #如果在init注册时没有传递前缀名，默认是/name
        for f,rule,options in self.mound:#将元祖自动解包成三个变量，f即视图函数
            endpoint = options.pop("endpoint", f.__name__)#f.name即视图 函数 的名字，没有传endpoint的话就默认是视图函数名字
            bp.add_url_rule(url_prefix+rule,endpoint,f,**options)#调用原有蓝图方法进行蓝图注册：重点
        pass