
from pyecharts import options as opts
from pyecharts.charts import Radar
import datetime,time

class arrayTograpg:
    def tograph(self,arrayVal,name) -> Radar:
        value_bj = [
            arrayVal

        ]



        c_schema = [
            {"name": "speed", "max": 100},
            {"name": "dribbling", "max": 100},
            {"name": "shooting", "max": 100},
            {"name": "passing", "max": 100},

            {"name": "defence", "max": 100},

            {"name": "physical", "max": 100},
            {"name": "gk_diving", "max": 100},
            {"name": "gk_positioning", "max": 100},
            {"name": "gk_reflexes", "max": 100},
            {"name": "gk_gk_handling", "max": 100},
            {"name": "gk_kicking", "max": 100},
        ]
        c = (
            Radar()
                .add_schema(schema=c_schema, shape="circle")
                .add(name, value_bj, color="#f9713c")

                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="Radar-Player"))
        )
        hname = str(time.time()) + '.html'

        c.render('./front-end/graph/'+hname)
        return hname

    def tographt(self,arrayVal,name) -> Radar:
        value_bj = [
            arrayVal

        ]



        c_schema = [
            {"name": "buildUpPlaySpeed", "max": 100},
            {"name": "buildUpPlayDribbling", "max": 100},
            {"name": "buildUpPlayPassing", "max": 100},
            {"name": "chanceCreationCrossing", "max": 100},

            {"name": "chanceCreationPassing", "max": 100},

            {"name": "chanceCreationShooting", "max": 100},
            {"name": "defenceAggression", "max": 100},
            {"name": "defencePressure", "max": 100},
            {"name": "defenceTeamWidth", "max": 100},
        ]
        c = (
            Radar()
                .add_schema(schema=c_schema, shape="circle")
                .add(name, value_bj, color="#f9713c")

                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="Radar-Player"))
        )
        hname = str(time.time()) + '.html'

        c.render('./front-end/graph/'+hname)
        return hname