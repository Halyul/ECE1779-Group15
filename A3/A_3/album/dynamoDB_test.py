from datetime import datetime

from album.aws.dynamoDB_admin import db_get_image_by_key_admin, db_get_all_images_admin
from album.aws.dynamoDB_common import db_upload_image, db_delete_image, db_set_is_shared, db_update_access_time, \
    db_get_shared_link_table_attributes, STATISTICS_TABLE, CAPACITY, \
    db_get_stats_from_table
from album.aws.dynamoDB_table import db_create_table_stats, db_intiate_stats_table
from album.aws.dynamoDB_user import db_is_allowed_get_shared_image, db_get_image_by_key_user, db_get_all_images_user
from album.aws.testOnly import db_set_tag, db_set_thumbnail

now = datetime.now()
time_stamp = str(now.strftime("%Y-%m-%d %H:%M:%S"))

# 1. Upload image
# db_upload_image("1", "image1", "user1", time_stamp)
# db_upload_image("2", "image2", "user1", time_stamp)
# db_upload_image("3", "image3", "user3", time_stamp)
# db_upload_image("4", "image3", "user4", time_stamp)
# db_set_tag("1", "tag1")
# db_set_tag("2", "tag1")
# db_set_tag("3", "tag1")
# db_set_tag("4", "tag1")
# db_set_thumbnail("1", "thumb1")
# db_set_thumbnail("2", "thumb2")
# db_set_thumbnail("3", "thumb3")
# db_set_thumbnail("4", "thumb4")

# 2. Get image based on key
# print(db_get_image_attributes_by_key_admin('1').get('Image'))
# print(db_get_image_attributes_by_key_user('user1', '1'))

# 3. Delete image
# db_delete_image('3')

# 4. Share image
# db_set_is_shared('z', 'False')

# 5. Update access time
# db_update_access_time('1', time_stamp)

# 6. Get shared image
# print(db_is_allowed_get_shared_image('2'))

# 7. Get all thumbnails
# print(db_list_all_records_admin('Image', 'ImageIndex'))
# print(db_list_all_records_user('user1', 'Image'))

# 8. List all attributes
# print(db_list_all_records_attributes_admin())
# print(db_list_all_records_attributes_user('user1'))

# 9. Get thumbnails by tag
# content = []
# results = db_get_image_attributes_by_tags_admin('tag1')
# for result in results:
#     content.append(result.get('Thumbnail'))
# print(content)
# print(db_get_image_attributes_by_tags_user('user1', 'tag1'))

# 10. Remove all images
# db_delete_all_images_admin()

# 11. Get shared_link table
# print(db_get_shared_link_table_attributes('1'))

# 12 Get image by key
# print(db_get_image_by_key_user('user1', '1'))
# print(db_get_image_by_key_admin('1'))

# 13 Get all images user
# print(db_get_all_images_user('user1'))
# print(db_get_all_images_admin())
# db_create_table_stats()
# db_intiate_stats_table()
# update_num_calls_statistics()

# print(db_get_image_by_key_admin('1'))

print(db_get_stats_from_table(CAPACITY))
# print(db_get_item_from_table(STATISTICS_TABLE, 'Statistics', 'Number of Calls to Lambda Function'))