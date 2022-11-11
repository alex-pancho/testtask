import requests
import json
import unittest
'''
## Test get users API
Host: https://reqres.in
Path: /api/users
Parameter: page
Method: GET
'''

host = "https://reqres.in"


def get_users_page(page_number: int):
    path = "/api/users"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " + \
                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36",
              }
    query = {"page":page_number}
    r = requests.get(host+path, headers=headers, params=query)
    try:
        return r.json()
    except json.JSONDecodeError:
        return {}

def get_user_full_name_list(start:int, end:int):
    if not isinstance(start, int) or not isinstance(end, int):
        return []
    elif end < start or start > 12 or end > 12:
        return []
    users_p1 = get_users_page(1).get("data")
    if start >= 6 or end > 6:
        users_p2 = get_users_page(2).get("data")
        users_p1.extend(users_p2)
    returned_list = users_p1[start-1:end]
    users_list = []
    for u in returned_list:
        users_list.append(f'{u.get("first_name")} {u.get("last_name")}')
    users_list.sort()
    return users_list


class Endpoint1PositiveTest(unittest.TestCase):
    
    def test_a_first_part(self):
        """Select set with first part"""
        ul = get_user_full_name_list(1,3)
        expected = ['Emma Wong', 'George Bluth', 'Janet Weaver']
        self.assertEqual(ul, expected)
    
    def test_b_first_second_part(self):
        """Select set with first and second part"""
        ul = get_user_full_name_list(5,8)
        expected = ['Charles Morris', 'Lindsay Ferguson', 'Michael Lawson', 'Tracey Ramos']
        self.assertEqual(ul, expected)
    
    def test_c_all_items(self):
        """Select all items to set"""
        ul = get_user_full_name_list(1,12)
        expected = ['Byron Fields', 'Charles Morris', 'Emma Wong', 'Eve Holt', 'George Bluth',
                    'George Edwards', 'Janet Weaver', 'Lindsay Ferguson', 'Michael Lawson', 
                    'Rachel Howell', 'Tobias Funke', 'Tracey Ramos']
        self.assertEqual(ul, expected)


class Endpoint2NegativeTest(unittest.TestCase):
    
    def test_d_start_less_end(self):
        """Wrong input: start less then end"""
        ul = get_user_full_name_list(5,3)
        expected = []
        self.assertEqual(ul, expected)
    
    def test_e_out_of_range(self):
        """Wrong input: out of range"""
        ul = get_user_full_name_list(5,13)
        expected = []
        self.assertEqual(ul, expected)
    
    def test_f_not_int_input(self):
        """Wrong input: not int"""
        ul = get_user_full_name_list("a","3.15")
        expected = []
        self.assertEqual(ul, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
