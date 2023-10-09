"""
Refactor the next function using yield to return the array of objects found by the
`s3.list_objects_v2` function that matches the given prefix.
"""
def get_s3_objects(bucket, prefix=''):
    s3 = boto3.client('s3')

    kwargs = {'Bucket': bucket}
    # Optional: limit number of results to N
    # kwargs = {'MaxKeys': N}
    next_token = None
    if prefix:
        kwargs['Prefix'] = prefix

    while True:
        if next_token:
            kwargs['ContinuationToken'] = next_token
        resp = s3.list_objects_v2(**kwargs)
        contents = resp.get('Contents', [])
        for obj in contents:
            key = obj['Key']
            if key.startswith(prefix):
                yield obj
        next_token = resp.get('NextContinuationToken', None)

        if not next_token:
            break



"""
Please, full explain this function: document iterations, conditionals, and the
function as a whole
"""

def fn(main_plan, obj, extensions=[]):
    """
    function returns the items list, which contains the products data processed from obj input, main plan, and the extensions information

    Parameters
    ----------
    main_plan: object containing the main plan
    obj: object containing the items' data
    extensions: list of objects containing plan extensions (optional, default empty list)
    """

    # items: stores procesed data by appending one by one
    items = []
    # sp: boolean, indicates if the main plan is found on 'obj' data
    sp = False
    # cd: boolean, indicates if the 'obj' data contains any deleted products
    cd = False
    # ext_p: stores processed price id and qty for the extensions
    ext_p = {}

    # Save extensions plans to a key/value dictionary for easier access later in the process.
    for ext in extensions:
        ext_p[ext['price'].id] = ext['qty']

    # Process items data from 'obj' and map it into 'items'
    for item in obj['items'].data:
        # current product details
        product = {
            'id': item.id
        }

        if item.price.id != main_plan.id and item.price.id not in ext_p:
            # Price not found in the extensions or main plan, consider the product deleted.
            product['deleted'] = True
            cd = True
        elif item.price.id in ext_p:
            # Price found in the extensions
            qty = ext_p[item.price.id]
            if qty < 1:
                # Qty less than 1, consider the product deleted.
                product['deleted'] = True
            else:
                #  save product qty, given qty > 1
                product['qty'] = qty
            # Process complete! Remove price id from ext_p to avoid re-using the extension data
            del ext_p[item.price.id]
        elif item.price.id == main_plan.id:
            # Mark main plan found on 'obj' data
            sp = True

        # Store products in 'items' list
        items.append(product)

    if not sp:
        # if sp is still False, the main plan was not found,add it to the items list with qty 1
        items.append({
            'id': main_plan.id,
            'qty': 1
        })

    for price, qty in ext_p.items():
        # Process remaining extensions plans not found in the 'obj', if any, data add it to the items list if qty > 1
        if qty < 1:
            continue
        items.append({
            'id': price,
            'qty': qty
        })

    return items


"""
Having the class `Caller` and the function `fn`
Refactor the function `fn` to execute any method from `Caller` using the argument `fn_to_call`
reducing the `fn` function to only one line.
"""
class Caller:
    add = lambda a, b : a + b
    concat = lambda a, b : f'{a},{b}'
    divide = lambda a, b : a / b
    multiply = lambda a, b : a * b

def fn(fn_to_call, *args):
    return getattr(Caller, fn_to_call)(*args)


"""
A video transcoder was implemented with different presets to process different videos in the application. The videos should be
encoded with a given configuration done by this function. Can you explain what this function is detecting from the params
and returning based in its conditionals?
"""
def fn(config, w, h):
    v = None
    # Display Aspect ratio
    ar = w / h

    # Horizontal/Rectangular, e.g 9" height / 16" width
    if ar < 1:
        v = [r for r in config['p'] if r['width'] <= w]
    # Vertical/Rectangular, e.g. 16" height / 9" width
    elif ar > 4 / 3:
        v = [r for r in config['l'] if r['width'] <= w]
    # Standard/Square, e.g. 9/9, 1/1
    else:
        v = [r for r in config['s'] if r['width'] <= w]

    # Solution:
    # fn returns a list of resources based on current display's height/width, e.g. config represents a list of resources based on:
    # config['p'], contains assets best viewed on portrait resolutions.
    # config['l'], contains assets best viewed on landscape resolutions.
    # config['s'], contains assets best viewed on square resolutions.
    return v

"""
Having the next helper, please implement a refactor to perform the API call using one method instead of rewriting the code
in the other methods.
"""

from requests import request
class Helper:
    DOMAIN = 'http://example.com'
    SEARCH_IMAGES_ENDPOINT = 'search/images'
    GET_IMAGE_ENDPOINT = 'image'
    DOWNLOAD_IMAGE_ENDPOINT = 'downloads/images'

    AUTHORIZATION_TOKEN = {
        'access_token': None,
        'token_type': None,
        'expires_in': 0,
        'refresh_token': None
    }

    def get_request(self, url, method='get', **kwargs):
        token_type = self.AUTHORIZATION_TOKEN['token_type']
        access_token = self.AUTHORIZATION_TOKEN['access_token']

        headers = {
            'Authorization': f'{token_type} {access_token}',
        }

        try:
            return request(method, url, headers=headers, **kwargs)
        except:
            print("Error with the API")

    def search_images(self, **kwargs):
        URL = f'{self.DOMAIN}/{self.SEARCH_IMAGES_ENDPOINT}'
        response = self.get_request(URL, params = kwargs)
        return response

    def get_image(self, image_id, **kwargs):
        URL = f'{self.DOMAIN}/{self.GET_IMAGE_ENDPOINT}/{image_id}'
        response = self.get_request(URL, params = kwargs)
        return response

    def download_image(self, image_id, **kwargs):
        URL = f'{self.DOMAIN}/{self.DOWNLOAD_IMAGE_ENDPOINT}/{image_id}'
        response = self.get_request(URL, 'post', data = kwargs)
        return response
