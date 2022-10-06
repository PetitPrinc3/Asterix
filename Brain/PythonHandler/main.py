from PywavaAutomation import main

main.main()




# # Get results
#     info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Fetching results')


#     ctnt = {
#                     'ind_results': []
#                 }


#     with open("clean.json", "w") as results:

#         results.seek(0)

#         js = json.dumps(ctnt, indent=4)

#         results.write(js)

#     sftp.get('\\Users\\ac-center\\Desktop\\PywavaAutomation\\Pywava\\scan_results.json', 'scan_results.json')

#     res = fr.get_stats('scan_results.json')

#     with open('clean.json', 'r+') as outp:

#         files = []

#         for suc in res[0]:
#             success(f'File {suc["PATH"]} is clean.')
#             files.append(suc)

#         js = json.load(outp)

#         js['ind_results'] = files

#         outp.seek(0)

#         js = json.dumps(js, indent = 4)

#         outp.write(js)

#     print()

#     if len(res[1]) > 0:

#         for fai in res[1]:
#             fail(f'File {fai["PATH"]} were flagged as malicious.')

#         print()
#         print("Do you wish to try and sanitize the files ? (Y/n)")

#         while True:
#             choice = str(input('>>> '))[0].lower()

#             if choice == 'y':
#                 san = True
#                 break

#             elif choice == 'n':
#                 san = False
#                 break

#             else:
#                 fail('Choice failed, try again.')