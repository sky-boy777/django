# 为了将在数据库查询出来的对象转换成json数据返回给前端，简化了手动转换的步骤
from rest_framework import serializers  # 序列化器
from app.models import Data
import re

# # 自定义序列化器，如果要保存，则需要实现update方法跟create方法
# class QbSerializers(serializers.Serializer):
#     id = serializers.IntegerField()
#     text = serializers.CharField(error_messages={
#         '验证': '未通过抛出的异常信息，跟django内置表单验证一样',
#     })
#
# # 重写父类方法
#     # 保存            已验证的数据
#     def create(self, validated_data):
#         ds = Data(text=validated_data.get('text'))  # 首先查看数据库里有没有相同的数据，相同则更新
#         ds.text = validated_data.get('text')
#         ds.save()
#         return ds
#         # return Data.objects.create(**validated_data)  这样的话必须保证validated_data的数据跟表的字段一一对应
#
#     # 更新            要更新对象   已验证的数据
#     def update(self, instance, validated_data):
#         """
#
#         :param instance: 要更新的对象
#         :param validated_data: 更新的属性
#         :return: 对象
#         """
#         # 更新逻辑
#
#         # 保存
#         instance.save()
#         return instance




# 通过模型生成序列化器, 自动生成update跟create方法
from app.models import Data

# # 自定义函数验证
def text_yanzheng(value):
    if len(value) < 3:
        raise serializers.ValidationError('字数不能少于三个')

class QbSerializers(serializers.ModelSerializer):

    # 调用自定义验证函数,验证text字段，字段必须跟模型里的字段名一致
    text = serializers.CharField(validators=[text_yanzheng])

    class Meta:
        model = Data  # 模型类
        fields = '__all__'  # 所有字段
        # fields = ['id', 'text']  # 自定义需要的字段，使用列表或元组： fields = ('id', 'text')
        # exclude = ['id']  # 排除的字段

    # 单字段验证：validate_字段名，value为字段形参
    def validate_text(self, value):
        # 验证
        if len(value) < 2:
            # 返回错误信息
            raise serializers.ValidationError('字数不能少于两个')
        return value

    # 验证多个字段，attrs为字段集
    def validate(self, attrs):
        # 验证
        if attrs['text'] == '0':
            raise serializers.ValidationError('不能输入0')
        if re.search(r'反政府', attrs['text']):  # 如果有不允许的字样，抛异常
            raise serializers.ValidationError('有不允许的字')
        return attrs


