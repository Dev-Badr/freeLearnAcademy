from django.shortcuts import render

def handler404(request):
	# # if exception:
 # #        logger.error(exception)
 #    url = request.get_full_path()
    return render(request, 'error_pages/error_page.html', status=404) # {'url':url,}


# def page_not_found_view(request, exception, template_name='error_page.html'):
#     if exception:
#         logger.error(exception)
#     url = request.get_full_path()
#     return render(request, template_name,
#                   {'message': '哎呀，您访问的地址 ' + url + ' 是一个未知的地方。请点击首页看看别的？', 'statuscode': '404'}, status=404)
