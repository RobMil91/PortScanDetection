

import ipaddress

#this modul is needed to balance a structure of folders with maps


def ip_to_int(str_ip):

    return int(ipaddress.IPv4Address(str_ip))

# x achsis buckets -> dataset get lowest and highest source IP calculate / 32 
def get_array_x_index(int_value_ip, buckets = 32.0):


    # print("int value ip: " + str(int(int_value_ip)))
    # float to int conversion? 

    #we use buckets -1 here, because there actually is 32 buckets but 0 is one of them so we technically have the max bucket at 31 (expl with 32x32)
    bucket_size = (ip_to_int("255.255.255.255") / (buckets - 1))

    # print("bucket_size: " + str(int(bucket_size)))


    # calculate ip / bucket size -> get index
    index = int_value_ip / (bucket_size)

    return int(index) 


def get_float_bucket_size(buckets = 32.0):
    return (ip_to_int("255.255.255.255") / buckets)


#needed to convert a float step into a human readable (hr) format
def float_to_hr_IP(float_ip):

    str_step = str(float_ip)

    int_step = int(float(str_step))

    str_value_ip_hr = ipaddress.IPv4Address(int_step)


    return str_value_ip_hr


def iterate_each_bucket(buckets, stepsize):

    bash_array = "("

    for i in range(buckets):
        #used to get to the end of each bucket
        itr = i + 1

        #needed to be on lower end of bucket
        step = i * stepsize

        # print(float_to_hr_IP(step))

        #used to get in the middle of the bucket
        step_itr = itr * stepsize - stepsize * 0.5


        ip_hr = float_to_hr_IP(step_itr)

        # decimal_ip = ip_to_int(str(ip_hr)) 

        # print(decimal_ip)

        bash_array = bash_array + "'" +  str(ip_hr) + "'" + " "

        print(ip_hr)

    return bash_array[:len(bash_array) - 1] + ")"








# print(get_array_x_index(ip_to_int("255.255.255.255")))
# print(get_float_bucket_size())


string_bash = iterate_each_bucket(32, get_float_bucket_size())

print(string_bash)