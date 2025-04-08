class Properties(object):
    def __init__(self,fields=None):
        if fields == None : fields = {}
        self.fields =fields

    def add_title(self,field_name,field_value):
        self._add_field(field_name,field_value,'title')      
    
    def add_rich_text(self,field_name,field_value):
        self._add_field(field_name,field_value,'rich_text')
    def add_select(self,field_name,field_value):
        self._add_field(field_name,field_value,'select')
    def add_multi_select(self,field_name,field_value):
        self._add_field(field_name,field_value,'multi_select')

    def add_date(self,field_name,field_value):
        self._add_field(field_name,field_value,'date')

    def add_checkbox(self,field_name,field_value):
        self._add_field(field_name,bool(field_value),'checkbox')

    def add_number(self,field_name,field_value):
        self._add_field(field_name,float(field_value),'number')

    def add_url(self,field_name,field_value):
        self._add_field(field_name,field_value,'url')
    
    def add_status(self,field_name,field_value):
        self._add_field(field_name,field_value,'status')

    def _add_field(self,field_name,field_value,field_type):
        self.fields[field_name]= (field_type,field_value)

    # 新增方法：让类支持 items() 访问
    def items(self):
        return self.fields.items()