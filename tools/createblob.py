from azure.storage.blob import BlockBlobService, ContentSettings

block_blob_service = BlockBlobService(account_name='photofunstorage', account_key='Br6qGU0woc+qOQtsneQ6XkgQx6gsmcvmbg9Eyh6+gpISHwmu48o+rmBzIQvOkYfho5FM3xsDP1TrKWVr08XQMg==')

block_blob_service.create_container('mergedarts')
"""
block_blob_service.create_blob_from_path(
    'styles', 'style1','static/img/qingming.jpg', content_settings=ContentSettings(content_type='image/jpg')
)

block_blob_service.create_blob_from_path(
    'styles', 'style2','static/img/hangongchunxiao.jpg', content_settings=ContentSettings(content_type='image/jpg')
)
block_blob_service.create_blob_from_path(
    'styles', 'style3','static/img/huachunshan.jpg', content_settings=ContentSettings(content_type='image/jpg')
)
block_blob_service.create_blob_from_path(
    'styles', 'style4','static/img/nanpingyaji.jpg', content_settings=ContentSettings(content_type='image/jpg')

)
block_blob_service.create_blob_from_path(
    'styles', 'style5','static/img/miyouren.jpg', content_settings=ContentSettings(content_type='image/jpg')
)
block_blob_service.create_blob_from_path(
    'styles', 'style6','static/img/wuguanzhong.jpg', content_settings=ContentSettings(content_type='image/jpg')
)
"""




