#from django.shortcuts import render
# tools/views.py

import shutil
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.serializers import serialize
from requests import request
import requests
from .models import ProjectDetail, res_customer_detail
import mysql.connector as sql
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse, urljoin
import os
import time
def register(request):
    return render(request,'register.html') 
def register_user(request):
        name =lname= email = password = mobile = None  # Initialize variables outside the try block
        try:
            con = sql.connect(host="localhost", user="root", passwd="Zainab.2001", database='make')
            cursor =con.cursor()
            d = request.POST
            for key, value in d.items():
                if key == "tfname":
                    name = value
                elif key == 'tlname':
                    lname=value
                elif key == 'tmail':
                    email = value
                elif key == 'pwd':
                    password = value
                elif key == 'mob':
                    mobile = value
        except:
            print()
        print("first name",name, "last name ",lname)
        # Explicitly specify the columns excluding 'id'
        query = "INSERT INTO make.res_customer_detail (fname,lname,mail,pwd,mob) VALUES (%s, %s, %s, %s,%s)"
        values = (name,lname,email,password,mobile)
        cursor.execute(query, values)
        con.commit()

        return render(request,'login.html',{})


def login(request):
    return render(request,'login.html', {})
import smtplib
from django.shortcuts import render, HttpResponse
import mysql.connector as sql

def login2(request):
    if request.method == 'POST':
        mail = request.POST.get('tmail')
        passwd = request.POST.get('tpass')

        # Your MySQL connection code here
        con = sql.connect(host="localhost", user="root", passwd="Zainab.2001", database='make')
        cr = con.cursor()
        print(mail,passwd)
        query = "SELECT cid, fname, mob FROM make.res_customer_detail WHERE mail=%s AND pwd=%s"
        print(cr.execute(query,(mail,passwd)))
        result = cr.fetchone()

        if result:
            user_id, user_name, user_phone = result
            request.session['uid'] = user_id
            request.session['uname'] = user_name
            request.session['mob'] = user_phone
            request.session['umail'] = mail
            print("Login successful for:", mail)
            print(user_id, "\n", user_name, "\n", user_phone)

            # Sending email after successful login
            try:
                HOST = "smtp.gmail.com"
                PORT = 587
                FROM_EMAIL = "webseo42@gmail.com"
                TO_EMAIL = mail
                PASSWORD = "zhlu iihq qkuc qlru"
                print("this mail from try box","\t",mail)

                # SUBJECT = "Thanks for the Register\n" 

                # "Hi" + user_name + ","+'\n'+"Your account has been created successfully."+'\n'

                

                # """Thanks,
                # Test Account
                # """
                SUBJECT="""Subject:Thank You for Registering",

                Dear,

                Thank you for registering.  We are excited to have you as part of our community.

                You've taken the first step towards.

                If you have any feedback or suggestions on how we can improve your experience, 
                please feel free to share them with us. We're always looking for ways to enhance our platform for our users.

                Once again, thank you for choosing US. We look forward to serving you.

                Warm regards,
                The [SEO Analysis] Team."""

                smtp = smtplib.SMTP(HOST, PORT)

                status_code, response = smtp.ehlo()
                print(f"[*] Echoing the server: {status_code} {response}")

                status_code, response = smtp.starttls()
                print(f"[*] Starting TLS connection: {status_code} {response}")

                status_code, response = smtp.login(FROM_EMAIL, PASSWORD)
                print(f"[*] Logging in: {status_code} {response}")

                smtp.sendmail(FROM_EMAIL, TO_EMAIL, SUBJECT)
                smtp.quit()


                print("Email sent after login.")

            except Exception as e:
                print("Failed to send email:", e)

            # You can do further processing here
            return render(request, "index.html", {'name': user_name})
        else:
            return HttpResponse("Invalid email or password")
    else:
        return HttpResponse("Method not allowed")

def index(request):
        uid=request.session.get('uid')
        uname=request.session.get('uname')
        umail=request.session.get('umail')
        phone=request.session.get('mob')
        print(uid,"\n",uname,"\n",umail,"\n",phone)
        return render(request,"index.html",{'name':uname})

def forgot(request):
    return render(request,'forgot_password.html')

def forgot2(request):
    mail=None
    mail=request.POST.get('mail')
    con=sql.connect(host="localhost",user="root",passwd="Zainab.2001",database='make')
    cr=con.cursor()
    if (cr or mail):
        query="select cid, fname, mob from make.res_customer_detail where mail=%s"
        cr.execute(query,(mail,))
        res=cr.fetchone()
        if(res):
            user_id,user_name,user_mob=res
            request.session['uid']=user_id
            request.session['uname']=user_name
            request.session['mob']=user_mob
            request.session['umail']=mail
            print(user_id,user_name,user_mob)
            return render(request,'index.html',{'name':user_name})
    return HttpResponse("you are our customer")
    #return render(request,"index.html")

def logout(request):
    request.session.clear()
    return render(request,"login.html")

def myprofile(request):
    con=sql.connect(host="localhost",user="root",passwd="Zainab.2001",database='make')
    cur=con.cursor()
    uid=request.session.get('uid')
    try:
        query="select * from make.res_customer_detail where cid=%s"
        cur.execute(query,(uid,))
        data=cur.fetchone()
        user_data={
                'cid' : data[0],
                'cname' : data[1],
                'clname':data[2],
                'cmail' : data[3],
                'cmob' : data[5]
                }
        print(user_data)
        return render(request,'myprofile.html',{'info':user_data})
    except:
            return render(request,'myprofile.html')

def allcustomer(request, *args, **kwargs):
    #customers=customer.objects.get(id=1)
    # data=list(customer.objects.values())
    # return JsonResponse({'data':data})
    # con=sql.connect(host="localhost",user="root",passwd="Zainab.2001",database="website")   
    # cursor=con.cursor()
    # query="SELECT * FROM `website`.`res_customer_detail`"
    # cursor.execute(query)
    # data=list(cursor.fetchall())
    # context={'data':data}
    # return render(request,'record.html',context)
    #return render(request,'record.html',{'customers':customers})
    return render(request,'record.html')
# def editprofile(request):
#     return (request,'edit.html')
# def edit2(request):
#         uname=umail=ulname=uphone=None
#         uname=request.POST.get('efname')
#         print(uname)
#         return HttpResponse("this is the edit2 page")

def editprofile(request):
    uname=request.session.get('uname')
    return render(request, 'editprofile.html',{'name':uname})

def edit2(request):
    uname = umail = ulname = uphone = None
    
    # Get POST data
    uname = request.POST.get('efname')
    ulname = request.POST.get('elname')
    umail = request.POST.get('eumail')
    uphone = request.POST.get('econ')
    
    # Get user ID from session
    uid = request.session.get('uid')

    try:
        # Connect to the database
        con = sql.connect(host="localhost", user="root", passwd="Zainab.2001", database="make")
        cr = con.cursor()

        # Update user details in the database
        query = "UPDATE make.res_customer_detail SET fname=%s, lname=%s, mail=%s, mob=%s WHERE cid=%s"
        cr.execute(query, (uname, ulname, umail, uphone, uid))

        # Commit changes to the database
        con.commit()

        print("Update successful")

    except sql.Error as e:
        print("Error updating user details:", e)
        # You might want to handle the error more gracefully, e.g., return an error response

    finally:
        # Close database connection
        if con:
            con.close()

    return render(request,'myprofile.html')

def changepassword(request):
    return render (request,"changepassword.html")

def change(request):
    email=pass1=pass2=None
    email=request.POST.get('umail')
    pass1=request.POST.get('pass1')
    pass2=request.POST.get('pass2')
    uid=request.session.get('uid')
    print(email,pass1,pass2,uid)
    con=sql.connect(host="localhost",user="root",passwd="Zainab.2001",database="make")
    cur=con.cursor()
    if (pass1==pass2):
        cur.execute("update make.res_customer_detail set pwd=%s where mail=%s and cid=%s",(pass1,email,uid))
        print("password is changed")
    return redirect(request,'login.html')

def add(request):
    username=request.session.get('uname')
    print("User Name \t",username)
    return render(request,'projectadd.html',{'username':username})


MAX_DIR_LENGTH = 50  # Maximum length of directory name
MAX_DEPTH = 3         # Maximum depth of crawling
visited_urls = set()
crawled_data = {}
def projectadd(request):
    username = request.session.get('uname')
    userid = int(request.session.get('uid'))
    print("from project add function",username,userid)
    if request.method == 'GET':
        return render(request, 'projectadd.html')
    elif request.method == 'POST':
        url = request.POST.get('purl')
        output_dir = request.POST.get('pname')
        status = request.POST.get('satus')
        print(url, output_dir, status, userid)
        
        if output_dir:
            con = sql.connect(host="localhost", user="root", password="Zainab.2001", database="make")
            cur = con.cursor()

            # Insert project details into the database
            query = "INSERT INTO make.tools_projectdetail (url, pname, status, user_id_id) VALUES (%s, %s, %s, %s)"
            cur.execute(query, (url, output_dir, status, userid))
            con.commit()

            # Fetch the last inserted project ID for the user
            q = "SELECT pid FROM make.tools_projectdetail WHERE user_id_id = %s "
            cur.execute(q, (userid,))
            last_inserted_pid = cur.fetchone()[0]  # Fetch the PID from the result tuple
            request.session['pid'] = last_inserted_pid
            print("Last inserted PID:", last_inserted_pid)

            # Adjusted caller function (projectadd)
            analysis_results,meta_specifications,content_info,media_list_info,https_info,mobile_optimization_info,frame_info,image_seo_info,additional_markup_info,social_networks_info,meta_tag_count,suggestions,average_score,analysis_result,ana,tag= crawl_website(url, output_dir)

            print(meta_specifications)
            # Render the result page
            return render(request, 'show.html',{
                'username': username,
                'analysis_results': analysis_results,
                'url': url,
                'meta_specifications'  : meta_specifications,
                'content_info':content_info,
                "media_list_info":media_list_info,
                "https_info":https_info,
                "mobile_optimization_info":mobile_optimization_info,
                "frame_info":frame_info,
                "image_seo_info":image_seo_info,
                "additional_markup_info":additional_markup_info,
                "social_networks_info":social_networks_info,
                "meta_tag_count":meta_tag_count,
                "suggestions": suggestions,
                "average_score":average_score,
                "analysis_result":analysis_result,
                "ana":ana,
                "tag":tag,
                
            })
                
        else:
            output_dir = 'links.txt'
            analysis_results, keyword_frequencies = crawl_website(url, output_dir)
            context = {
                'username': username,
                'analysis_results': analysis_results,
                'url': url,
                'keyword_frequencies': keyword_frequencies,
            }
            return render(request, 'show.html', context)
        
    return HttpResponse("The error in the code")

    return HttpResponse("The error in the code")

def crawl_website(url, output_dir):
            # Truncate directory name if it exceeds maximum length
            output_dir = output_dir[:MAX_DIR_LENGTH]

            # Create output directory with user-specified name
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Crawl the initial URL
        
            crawl_url_with_retry(url, output_dir, visited_urls, crawled_data, depth=0)

            # Check if crawled data is empty
            if not crawled_data:
                print("No data crawled. Check the crawling process.")
                return

            # Perform analysis and store results
            meta_information = calculate_meta_information(crawled_data)
            page_quality = calculate_page_quality(crawled_data)
            page_structure = calculate_page_structure(crawled_data)
            link_structure = calculate_link_structure(crawled_data)
            external_factors = calculate_external_factors(crawled_data)
            meta_tag_count = calculate_meta_tag_count(crawled_data)
            pages_with_image = calculate_pages_with_image(crawled_data)
            meta_specifications = extract_meta_specifications(url,crawled_data)
            content_info = extract_content_info(crawled_data)
            frame_info = extract_frame_info(crawled_data)
            mobile_optimization_info = extract_mobile_optimization_info(crawled_data)
            image_seo_info = extract_image_seo_info(crawled_data)
            social_networks_info = extract_social_networks_info(crawled_data)
            additional_markup_info = extract_additional_markup_info(crawled_data)
            https_info = extract_https_info(crawled_data)
            media_list_info = extract_media_list_info(crawled_data)
            analysis_results = seo_analysis(url)

    # Now you can use the results in your crawl_website function
            print("Analysis Result:")
            print(analysis_results)
            # print("Ana Result:")
            # print(ana)
            # print("Tag Result:")
            # print(tag)
            # print("Suggestion Result:")
            # print(sugess)
            # Print analysis results
            
            con = sql.connect(host="localhost", user="root", password="Zainab.2001", database="make")
            cur = con.cursor()

            # # Save CrawledData instance using raw SQL insert query
            # cur.execute("INSERT INTO make_tools_crawleddata (url, project_id) VALUES (%s, %s)", (url, project_id))
            # crawled_data_id = cur.lastrowid

            # # Save MetaInformation instance using raw SQL insert query
            # cur.execute("INSERT INTO make_tools_metainformation (crawled_data_id, meta_tag_count) VALUES (%s, %s)", (crawled_data_id, meta_tag_count))

            # # Save PageQuality instance using raw SQL insert query
            # cur.execute("INSERT INTO make_tools_pagequality (crawled_data_id, pages_with_image) VALUES (%s, %s)", (crawled_data_id, pages_with_image))

            # # Commit the transaction
            # con.commit()

            # # Close the database connection
            # cur.close()
            # con.close()
            #         # Combine all analysis results
            print("meta tag count:","\t",meta_tag_count,"pages with image:\t",pages_with_image)
            suggestions = generate_suggestions({
        "Meta information": meta_information,
        "Page quality": page_quality,
        "Page structure": page_structure,
        "Link structure": link_structure,
        "External factors": external_factors
    })
    
            analysis_results = {
                "Meta information": meta_information,
                "Page quality": page_quality,
                "Page structure": page_structure,
                "Link structure": link_structure,
                "External factors": external_factors
                                }
            analysis_result = {
        "Total pages analyzed": total_pages_analyzed,
        "Total meta descriptions found": len(total_meta_descriptions),
        "Total CSS files used": total_css_files
    }
            ana={
        "Total response time": total_response_time
            }
            tag={"Total heading structure": total_heading_counts}
            # if 'Improvements' in analysis_results:
            #     # sugess = analysis_results['Improvements']
                #print("Improvements:", sugess)
            total_score = analysis_results["Meta information"] + analysis_results["Page quality"] + analysis_results["Page structure"] + analysis_results["Link structure"] + analysis_results["External factors"]
            average_score = total_score / 5
            shutil.rmtree(output_dir)
            return analysis_results, meta_specifications, content_info, media_list_info, \
            https_info, mobile_optimization_info, frame_info, image_seo_info, \
            additional_markup_info, social_networks_info, meta_tag_count, suggestions, \
            average_score, analysis_result, ana, tag
            #return analysis_results,meta_specifications,content_info,media_list_info,https_info,mobile_optimization_info,frame_info,image_seo_info,additional_markup_info,social_networks_info,meta_tag_count,suggestions,average_score,analysis_result,ana,tag

# Initialize global variables to store aggregated analysis results
# import requests
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time

# Initialize global variables to store aggregated analysis results
total_meta_descriptions = []
total_css_files = 0
total_heading_counts = {f'h{i}': 0 for i in range(1, 7)}
total_response_time = 0
total_pages_analyzed = 0

# Function to fetch the webpage content
def fetch_page(url):
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        print(f"Error fetching page {url}: {e}")
        return None

# Function to parse the HTML and extract meta description tags
def extract_meta_descriptions(html):
    soup = BeautifulSoup(html, 'html.parser')
    meta_tags = soup.find_all('meta', attrs={'name': 'description'})
    return [tag['content'] for tag in meta_tags]

# Function to count the number of CSS files used
def count_css_files(html):
    soup = BeautifulSoup(html, 'html.parser')
    css_links = soup.find_all('link', attrs={'rel': 'stylesheet'})
    return len(css_links)

# Function to analyze heading structure
def analyze_heading_structure(html):
    soup = BeautifulSoup(html, 'html.parser')
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    heading_counts = {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 7)}
    return heading_counts

# Function to measure page response time
def measure_response_time(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    return end_time - start_time

# Function to extract internal links from HTML
def extract_internal_links(html, base_url):
    internal_links = []
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a', href=True):
        absolute_link = urljoin(base_url, link['href'])
        parsed_link = urlparse(absolute_link)
        if parsed_link.netloc == urlparse(base_url).netloc:
            internal_links.append(absolute_link)
    return internal_links

# Function to fetch CSS files from the webpage
def fetch_css_files(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        css_files = [urljoin(url, link['href']) for link in soup.find_all('link', rel='stylesheet')]
        return css_files
    except Exception as e:
        print(f"Error fetching CSS files from {url}: {e}")
        return []

# Function to analyze CSS file count and provide suggestions
def analyze_css_file_count(url):
    css_files = fetch_css_files(url)
    css_file_count = len(css_files)
    
    return css_file_count

# Function to generate SEO improvement suggestions
def generate_seo_improvement_suggestions(css_file_count, heading_structure_analysis, response_time, promote_in_social_networks):
    suggestions = []

    # Task 1: Try to reduce the number of used CSS files
    if css_file_count > 3:  # You can adjust the threshold as needed
        suggestions.append("Try to reduce the number of used CSS files to improve page loading speed. (Tip: Combine CSS files)")

    # Task 2: Review and improve the heading structure
    # You can provide specific suggestions based on the heading structure analysis
    if total_heading_counts['h1'] == 0:
        suggestions.append("Add at least one <h1> heading for better SEO. (Tip: Improve Heading Structure)")

    # Task 3: Improve the page response time
    if response_time > 3:  # You can adjust the threshold as needed
        suggestions.append("Optimize page elements and server performance to improve response time. (Tip: Optimize Page)")

    # Task 4: Promote your page in social networks
    if promote_in_social_networks:
        suggestions.append("Promote your page on social networks to increase visibility and traffic. (Tip: Promote on Social Networks)")

    return suggestions

# Function to perform SEO analysis for a website
def seo_analysis(url):
    global total_meta_descriptions, total_css_files, total_heading_counts, total_response_time, total_pages_analyzed

    visited_urls = set()

    def crawl_and_analyze(url):
        global total_css_files, total_response_time, total_pages_analyzed

        if url in visited_urls:
            return
        visited_urls.add(url)

        print(f"Analyzing page: {url}")
        html = fetch_page(url)
        if html:
            meta_descriptions = extract_meta_descriptions(html)
            total_meta_descriptions.extend(meta_descriptions)
            total_css_files += count_css_files(html)
            heading_structure_analysis = analyze_heading_structure(html)
            for tag, count in heading_structure_analysis.items():
                total_heading_counts[tag] += count
            total_response_time += measure_response_time(url)
            total_pages_analyzed += 1

            internal_links = extract_internal_links(html, url)
            for link in internal_links:
                crawl_and_analyze(link)

    crawl_and_analyze(url)

    # Analyze CSS file count and provide suggestions
    css_file_count = analyze_css_file_count(url)
    css_suggestions = generate_seo_improvement_suggestions(css_file_count, total_heading_counts, total_response_time, True)

    # Return the analysis results and suggestions
    return {
        "Total pages analyzed": total_pages_analyzed,
        "Total meta descriptions found": len(total_meta_descriptions),
        "Total CSS files used": total_css_files,
        "Total response time": total_response_time,
        "Total heading structure": total_heading_counts,
        "Improvements": css_suggestions
    }

# Example usage
#url = "https://arthjobconsultancy.com"  # Change this to the URL you want to analyze
# Print the analysis result


def generate_suggestions(analysis_results):
    suggestions = []

    # Example suggestion logic based on analysis results
    if analysis_results["Meta information"] < 50:
        suggestions.append("Improve meta tag descriptions and keywords for better search engine visibility.")
    if analysis_results["Page quality"] < 50:
        suggestions.append("Improve page quality by adding more engaging content, such as images and videos.")
    if analysis_results["Page structure"] < 70:
        suggestions.append("Enhance page structure by adding more hierarchical headings (h1, h2, etc.).")
    if analysis_results["Link structure"] < 60:
        suggestions.append("Optimize link structure by adding more internal links for better site navigation.")
    if analysis_results["External factors"] < 40:
        suggestions.append("Improve external factors by acquiring quality backlinks and enhancing social media presence.")

    return suggestions
def extract_media_list_info(crawled_data):
    image_count = 0
    link_count = 0
    for data in crawled_data.values():
        tags_data = data.get("tags_data", {})
        for tag_info in tags_data.values():
            if tag_info["name"] == "img":
                image_count += 1
            elif tag_info["name"] == "a":
                link_count += 1
    return {"image_count": image_count, "link_count": link_count}

def count_keyword_frequencies(crawled_data):
    keyword_frequencies = {}
    for data in crawled_data.values():
        tags_data = data.get("tags_data", {})
        for tag_info in tags_data.values():
            if tag_info["name"] == "p":  # Assuming you want to count keywords in paragraph tags
                text = tag_info.get("text", "").lower()  # Convert text to lowercase for case-insensitive matching
                words = text.split()  # Split text into words
                for word in words:
                    # Increment keyword frequency count
                    keyword_frequencies[word] = keyword_frequencies.get(word, 0) + 1
    return keyword_frequencies
def crawl_url_with_retry(url, output_dir, visited_urls, crawled_data, depth, max_retries=3):
            retries = 0
            while retries < max_retries:
                try:
                    crawl_url(url, output_dir, visited_urls, crawled_data, depth)
                    break  # If successful, break out of the retry loop
                except (HTTPError, URLError) as e:
                    print(f"Error fetching URL {url}: {e}")
                    retries += 1
                    time.sleep(5)  # Add a delay before retrying
            else:
                print(f"Failed to fetch URL {url} after {max_retries} retries")

def crawl_url(url, output_dir, visited_urls, crawled_data, depth):
            if depth >= MAX_DEPTH:
                return

            if url in visited_urls:
                return
            visited_urls.add(url)

            # Fetch webpage content
            try:
                req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                html_content = urlopen(req).read()
            except HTTPError as e:
                print(f"Error fetching URL {url}: {e}")
                log_error(url, f"HTTP Error: {e.code}")
                return
            except URLError as e:
                print(f"Error fetching URL {url}: {e.reason}")
                log_error(url, f"URL Error: {e.reason}")
                return
            except Exception as e:
                print(f"Error fetching URL {url}: {e}")
                log_error(url, f"Error: {e}")
                return

            # Extract tags and their information
            soup = BeautifulSoup(html_content, 'html.parser')
            tags_data = {}
            for tag in soup.find_all():
                tag_name = tag.name
                tag_attributes = tag.attrs  # Fetch attributes of the tag
                tag_text = tag.text.strip() if tag.text else None  # Fetch text of the tag
                tag_info = {
                    "name": tag_name,
                    "attributes": tag_attributes,
                    "text": tag_text
                }
                tags_data[tag_name] = tag_info

            # Store tags data along with the URL
            crawled_data[url] = {"url": url, "tags_data": tags_data}  # Include URL in the crawled data

            # Create directory for this URL
            url_directory = os.path.join(output_dir, urlparse(url).netloc)
            if not os.path.exists(url_directory):
                os.makedirs(url_directory)

            # Write tags data to JSON file
            filename = os.path.join(url_directory, urlparse(url).path.strip("/").replace("/", "_") + ".json")
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump({"url": url, "tags_data": tags_data}, json_file, ensure_ascii=False, indent=4)

            # Find and crawl links on the webpage
            for link in soup.find_all('a', href=True):
                child_url = urljoin(url, link['href'])
                crawl_url_with_retry(child_url, output_dir, visited_urls, crawled_data, depth + 1)
def extract_meta_specifications(url,crawled_data):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract meta tag information
    meta_information = {}
    
    # Extract title tag
    title_tag = soup.title
    if title_tag:
        meta_information["title"] = title_tag.string.strip()
    else:
        meta_information["title"] = "Title not found"
    
    # Extract meta description tag
    meta_description_tag = soup.find('meta', attrs={'name': 'description'})
    if meta_description_tag:
        meta_information["meta_description"] = meta_description_tag.get('content').strip()
    else:
        meta_information["meta_description"] = "Meta Description not found"
    
    # Extract meta keywords tag
    meta_keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
    if meta_keywords_tag:
        meta_information["meta_keywords"] = meta_keywords_tag.get('content').strip()
    else:
        meta_information["meta_keywords"] = "Meta Keywords not found"
    
    # Extract canonical URL
    canonical_tag = soup.find('link', attrs={'rel': 'canonical'})
    if canonical_tag:
        meta_information["canonical_url"] = canonical_tag.get('href').strip()
    else:
        meta_information["canonical_url"] = "Canonical URL not found"
    
    # Extract language
    language_tag = soup.find('html')
    if language_tag and 'lang' in language_tag.attrs:
        meta_information["language"] = language_tag['lang'].strip()
    else:
        meta_information["language"] = "Language not found"
    
    return meta_information

def log_error(url, error_message):
            #dirc=request.session.get('pname')
            
            error_filename = "crawl_errors.txt"
            with open(error_filename, 'a', encoding='utf-8') as file:
                file.write(f"URL: {url}\nError: {error_message}\n\n")

def analyze_and_store_results(output_dir, crawled_data):
            # Placeholder functions for calculating SEO analysis metrics
            meta_information = calculate_meta_information(crawled_data)
            page_quality = calculate_page_quality(crawled_data)
            page_structure = calculate_page_structure(crawled_data)
            link_structure = calculate_link_structure(crawled_data)
            server_info = calculate_server_info(crawled_data)
            external_factors = calculate_external_factors(crawled_data)

            # Combine all analysis results
            analysis_results = {
                "Meta information": meta_information,
                "Page quality": page_quality,
                "Page structure": page_structure,
                "Link structure": link_structure,
                "Server": server_info,
                "External factors": external_factors
            }
            context = {
            'analysis_results': analysis_results  # Pass analysis results to the template
        }

            # Print analysis results to console
            print("Analysis Results:")
            print("------------------")
            for aspect, score in analysis_results.items():
                print(f"{aspect}: {score}%")
            return render(request,'show.html',context)

def calculate_meta_information(crawled_data):
            # Placeholder implementation for calculating Meta information score
            # Example: Count the number of meta tags with name attribute
            print("Length of crawled_data:", len(crawled_data))  # Debug statement
            meta_tag_count = 0
            if crawled_data:
                for data in crawled_data.values():
                    tags_data = data.get("tags_data", {})
                    for tag_info in tags_data.values():
                        if tag_info["name"] == "meta" and "name" in tag_info["attributes"]:
                            meta_tag_count += 1
            
                # Score calculation based on the number of meta tags
                meta_information_score = (meta_tag_count / len(crawled_data)) * 100
                return meta_information_score
            else:
                return 0  # Return 0 if crawled_data is empty



def calculate_page_quality(crawled_data):
            # Placeholder implementation for calculating Page quality score
            # Example: Calculate the percentage of pages with at least one image
            pages_with_image = sum(1 for data in crawled_data.values() if any(tag_info["name"] == "img" for tag_info in data.get("tags_data", {}).values()))
            page_quality_score = (pages_with_image / len(crawled_data)) * 100
            return page_quality_score


def calculate_page_structure(crawled_data):
            # Placeholder implementation for calculating Page structure score
            # Example: Calculate the average number of headings per page
            total_headings = sum(len([tag_info for tag_info in data.get("tags_data", {}).values() if tag_info["name"].startswith("h")]) for data in crawled_data.values())
            average_headings = total_headings / len(crawled_data)
            page_structure_score = (average_headings / 6) * 100  # Assuming h1 to h6
            return page_structure_score

def calculate_link_structure(crawled_data):
            # Placeholder implementation for calculating Link structure score
            # Example: Calculate the ratio of internal to external links
            num_internal_links = sum(1 for data in crawled_data.values() for tag_info in data.get("tags_data", {}).values() if tag_info["name"] == "a" and "href" in tag_info["attributes"] and urlparse(tag_info["attributes"]["href"]).netloc == urlparse(data["url"]).netloc)
            num_external_links = sum(1 for data in crawled_data.values() for tag_info in data.get("tags_data", {}).values() if tag_info["name"] == "a" and "href" in tag_info["attributes"] and urlparse(tag_info["attributes"]["href"]).netloc != urlparse(data["url"]).netloc)
            total_links = num_internal_links + num_external_links
            if total_links == 0:
                return 0
            link_structure_score = (num_internal_links / total_links) * 100
            return link_structure_score


def calculate_server_info(crawled_data):
            # Placeholder implementation for calculating Server info score
            # Example: Check if the website has a meta tag with http-equiv attribute
            has_http_equiv_meta = any("meta" in tag_info["name"] and "http-equiv" in tag_info["attributes"] for data in crawled_data.values() for tag_info in data.get("tags_data", {}).values())
            server_info_score = 100 if has_http_equiv_meta else 0
            return server_info_score


def calculate_external_factors(crawled_data):
            # Placeholder implementation for calculating External factors score
            # Example: Calculate the ratio of pages with external links
            pages_with_external_links = sum(1 for data in crawled_data.values() for tag_info in data.get("tags_data", {}).values() if tag_info["name"] == "a" and "href" in tag_info["attributes"] and urlparse(tag_info["attributes"]["href"]).netloc != urlparse(data["url"]).netloc)
            external_factors_score = (pages_with_external_links / len(crawled_data)) * 100
            return external_factors_score
# Function to calculate meta tag count from crawled data
def calculate_meta_tag_count(crawled_data):
    # Initialize count
    meta_tag_count = 0
    
    # Iterate over crawled data
    for page_url, page_data in crawled_data.items():
        # Retrieve tags data for the page
        tags_data = page_data.get("tags_data", {})
        # Check if meta tags are present and count them
        for tag_info in tags_data.values():
            if tag_info["name"] == "meta":
                meta_tag_count += 1
                
    return meta_tag_count

def calculate_pages_with_image(crawled_data):
    # Initialize count
    pages_with_image = 0
    
    # Iterate over crawled data
    for page_url, page_data in crawled_data.items():
        # Retrieve tags data for the page
        tags_data = page_data.get("tags_data", {})
        # Check if any image tags are present
        if any(tag_info["name"] == "img" for tag_info in tags_data.values()):
            pages_with_image += 1
    
    return pages_with_image
def extract_content_info(crawled_data):
    word_count = 0
    stop_word_count = 0
    stop_words = set(["a", "an", "the", ...])  # Define your list of stop words
    h1_words = set()
    paragraph_count = 0
    
    for data in crawled_data.values():
        tags_data = data.get("tags_data", {})
        for tag_info in tags_data.values():
            if tag_info["name"] == "p":
                paragraph_count += 1
                text = tag_info.get("text")
                if text:
                    text = text.lower()
                    words = text.split()
                    word_count += len(words)
                    stop_word_count += sum(1 for word in words if word in stop_words)
            elif tag_info["name"] == "h1":
                text = tag_info.get("text")
                if text:
                    text = text.lower()
                    h1_words.update(text.split())

    word_count_percentage = (word_count - stop_word_count) / word_count * 100 if word_count > 0 else 0
    h1_word_usage = all(word in h1_words for word in stop_words)

    return {
        "word_count": word_count,
        "stop_word_percentage": stop_word_count / word_count * 100 if word_count > 0 else 0,
        "keyword_usage": h1_word_usage,
        "h1_heading_usage": h1_word_usage,
        "paragraph_count": paragraph_count,
        "placeholder_check": False,  # Placeholder logic placeholder
        "duplicate_check": False,  # Duplicate check logic placeholder
        "average_sentence_length": 0,  # Average sentence length logic placeholder
    }

def extract_frame_info(crawled_data):
    frame_usage = any(tag_info["name"] == "frame" for data in crawled_data.values() for tag_info in data.get("tags_data", {}).values())
    return {"frame_usage": frame_usage}

def extract_mobile_optimization_info(crawled_data):
    apple_touch_icon_specification = any(link["attributes"].get("rel") == "apple-touch-icon" for data in crawled_data.values() for link in data.get("tags_data", {}).values())
    viewport_specification = any(tag_info["name"] == "meta" and tag_info["attributes"].get("name") == "viewport" for data in crawled_data.values() for tag_info in data.get("tags_data", {}).values())
    javascript_file_count = sum(1 for data in crawled_data.values() for tag_info in data.get("tags_data", {}).values() if tag_info["name"] == "script")
    return {
        "apple_touch_icon_specification": apple_touch_icon_specification,
        "viewport_specification": viewport_specification,
        "javascript_file_count": javascript_file_count,
    }

def extract_image_seo_info(crawled_data):
    alt_text_usage = all("alt" in tag_info["attributes"] for data in crawled_data.values() for tag_info in data.get("tags_data", {}).values() if tag_info["name"] == "img")
    return {"alt_text_usage": alt_text_usage}

def extract_social_networks_info(crawled_data):
    social_sharing_widgets = any(tag_info["name"] in ("div", "span") and tag_info["attributes"].get("class") == "social-share" for data in crawled_data.values() for tag_info in data.get("tags_data", {}).values())
    return {"social_sharing_widgets": social_sharing_widgets}

def extract_additional_markup_info(crawled_data):
    additional_markup_check = False  # Placeholder
    return {"additional_markup_check": additional_markup_check}

def extract_https_info(crawled_data):
    https_usage = all(url.startswith("https://") for url in crawled_data.keys())
    return {"https_usage": https_usage}

def projectadd2(request):
    return HttpResponse("this is the add2")
def projectdetail(request):
    username = request.session.get('uname')
    con = sql.connect(host="localhost", user="root", passwd="Zainab.2001", database='make')
    cur = con.cursor()
    uid = request.session.get('uid')
    print(uid)
    query = "SELECT pid, url, pname, status FROM make.tools_projectdetail WHERE user_id_id=%s"
    cur.execute(query, (uid,))
    data = cur.fetchall()
    if data:
        projects = []
        for row in data:
            project = {
                'pid': row[0],
                'url': row[1],
                'pname': row[2],
                'status':row[3]
            }
            projects.append(project)
        print(username)
        return render(request, "projects.html", {'username': username, 'projects': projects})
    else:
        return HttpResponse("User not found")

    
def faq(request):
    username = request.session.get('uname')
    return render(request,'faq.html',{'username':username})
def key(request):
    username = request.session.get('uname')
    return render(request,'key_word_search.html',{'username':username})
from django.shortcuts import render
from .ranking import crawl_websites  # Assuming your crawling function is defined in crawl.py

def keyword_occurrences(request):
    username = request.session.get('uname')
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        base_url = request.POST.get('base_url')
        # Crawl the website and count keyword occurrences
        keyword_occurrences = crawl_websites(base_url, keyword)

        # Pass the keyword occurrences data to the template
        context = {
            'keyword': keyword,
            'base_url': base_url,
            'keyword_occurrences': keyword_occurrences.items()
        }
        return render(request, 'keyword_occurrences.html', context,{'username':username})
def keyw(request):
    # Render the initial form   
    return render(request, 'keyword_occurrences.html')
def contacts(request):
    user_name=request.session.get('uname')
    return render(request,'contact.html',{'name':user_name})

from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        query = request.POST.get('query', '')

        # Sending email
        subject = 'New Contact Form Submission'
        message = f'Name: {name}\nEmail: {email}\nQuery: {query}'
        sender_email = settings.EMAIL_HOST_USER
        recipient_email = 'webseo42@gmail.com'
        send_mail(subject, message, sender_email, [recipient_email])

        return render(request, 'success.html')  # Create a success page or redirect
    else:
        return render(request, 'contact.html')
    # views.py

from django.shortcuts import render
from .utils import search_google

def keyword_rank_checker(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        domain = request.POST.get('domain')
        country = request.POST.get('country')
        city = request.POST.get('city')
        state = request.POST.get('state')

        keyword_info = search_google(keyword, domain, country, city, state)
        if keyword_info is not None:
            return render(request, 'rank_checker_results.html', {'keyword_info': keyword_info})
        else:
            error_message = "Failed to fetch search results. Please try again later."
            return render(request, 'rank_checker_form.html', {'error_message': error_message})
    else:
        return render(request, 'rank_checker_form.html')
def aboutus(request):
    
    username=request.session.get('uname')
    return render(request,'aboutus.html',{'username':username})

def loginadmin(request):
    return render(request,'adminlogin.html', {})
import smtplib
from django.shortcuts import render, HttpResponse
import mysql.connector as sql

def loginadmin2(request):
    if request.method == 'POST':
        mail = request.POST.get('tmail')
        passwd = request.POST.get('tpass')

        # Your MySQL connection code here
        con = sql.connect(host="localhost", user="root", passwd="Zainab.2001", database='make')
        cr = con.cursor()
        if cr:
            print(mail, passwd)
            query = "SELECT id, name, mobile FROM make.res_admin_detail WHERE email = %s AND psw = %s"

            try:
                re = cr.execute(query, (mail, passwd))
                if re:
                    print("here we go")
                    print(re)
                    # result = cr.fetchone()
                else:
                    print("No records found.")
            except sql.Error as e:
                print("An error occurred:", e)
        else:
            print("Unable to connect to the database.")

        # if result:
        #     user_id, user_name, user_phone = result
        #     request.session['aid'] = user_id
        #     request.session['aname'] = user_name
        #     request.session['amob'] = user_phone
        #     request.session['amail'] = mail
        #     print("Login successful for:", mail)
        #     print(user_id, "\n", user_name, "\n", user_phone)

        #     # You can do further processing here
        return render(request, "adminpanel.html")
    return HttpResponse("Not a POST request!") 
    #     else:
    #         return HttpResponse("Invalid email or password")
    # else:
    #return HttpResponse("Admin Successfully login .")
def adminprofile(request):
    return render(request,'adminprofile.html')
def users(request):
    return render(request,'users.html')
def editadminprofile(request):
    return render(request, 'adminedit.html')
def edit(request):
    return HttpResponse("Admin edit successful")