from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
import time

class arrayTotable:
    def totable(self,arrayAttr,arrayValue,name) -> Table:
        table = Table()

        headers =arrayAttr
        rows = [
            arrayValue
        ]
        table.add(headers, rows).set_global_opts(
            title_opts=ComponentTitleOpts(title="Table-Details", subtitle=name)
        )
        hname = str(time.time()) + '.html'

        table.render('./front-end/table/'+hname)
        return hname