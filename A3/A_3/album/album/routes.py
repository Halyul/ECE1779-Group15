from album import webapp, service
from album.message import response


@webapp.route('/api/photos', methods=['POST'])
@response
def list_all():
    return service.list_all_multi_attributes()


@webapp.route('/api/key', methods=['POST'])
@response
def get_image():
    return service.get_image_by_key()


@webapp.route('/api/key', methods=['DELETE'])
@response
def delete():
    return service.delete_image()


@webapp.route('/api/upload', methods=['POST'])
@response
def upload():
    return service.upload_image()


@webapp.route('/api/share', methods=['POST'])
@response
def share():
    return service.share_image()


@webapp.route('/api/stats', methods=['POST'])
@response
def get_stats():
    return

# @webapp.route('/api/image/attributes', methods=['POST'])
# def get_image_attributes():
#     return service.get_image_attributes_by_key()
