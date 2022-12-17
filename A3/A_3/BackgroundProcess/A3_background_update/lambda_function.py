import urllib.parse
from dynamo_funcs import get_new_key_from_image, set_key_image_table, set_shared_link_table, update_num_calls_statistics
from tagging import do_tag
from thumbnail import make_thumbnail
from s3_func import get_image_from_s3, save_image_to_s3

print('Loading function')


def lambda_handler(event, context):
    # Get the object from the event and show its content type
    new_image_name = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    # do all these operations if this new image is not thumbnail added by this function itself
    if 'thumbnail' not in new_image_name:
        # save the thumbnail to s3
        thumbnail_name = new_image_name.split('.')[0] + '_thumbnail.jpg'
        original_image_data = get_image_from_s3(new_image_name)
        thumbnail_image_data = make_thumbnail(original_image_data)
        save_image_to_s3(thumbnail_image_data, thumbnail_name)
    
        # get the image tag
        tag = do_tag(original_image_data)
    
        # update key_image table
        new_key = get_new_key_from_image(new_image_name)
        set_key_image_table(new_key, new_image_name, thumbnail_name, tag)
    
        # update shared_link table
        set_shared_link_table(new_key)
    
    # update statistics table
    update_num_calls_statistics()