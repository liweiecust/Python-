from http import cookiejar
import requests

from selenium import webdriver

sites=[
        'https://ibuild.yzw.cn/home/proprietary',
        'https://ibuild.yzw.cn/home/proprietary/10807',
        'https://ibuild.yzw.cn/mgt/#/',
        'https://ibuild.yzw.cn/mgt/#/project',
        'https://ibuild.yzw.cn/labor/#/labor/workerMgt',
        'https://ibuild.yzw.cn/mgt/#/admin/virus/ipqcRecord/21692',
        'https://ibuild.yzw.cn/api/videoRecord/detail/21692?t=/1632797575705',
        'https://ibuild.yzw.cn/mgt/#/custom/bigscreen/add?sysNo=26',
        'https://file.yzw.cn/ibuild/pages/project_02-l.jpg?v=0.5',
        'https://ibuild.yzw.cn/mgt/#/admin/oversea/event',
        'https://ibuild.yzw.cn/mgt/#/admin/oversea/honor',
        'https://ibuild.yzw.cn/mgt/#/admin/oversea/preview',
        'https://ibuild.yzw.cn/open/#/admin/productAdminMgt/adminHardwareDetail?sysNo=10765',
        'https://ibuild.yzw.cn/open/#/admin/productAdminMgt/adminHardwareDetail?sysNo=10800',
        'https://ibuild.yzw.cn/api/open/admin/product/detail',
        'https://ibuild.yzw.cn/mgt/#/project/portalWebConfig/productTrends',
        'https://ibuild.yzw.cn/mgt/#/project/portalWebConfig/applicationIntro',
        'https://ibuild.yzw.cn/mgt/#/project/portalWebConfig/exampleIntro/exampleAdd?appSysNo=2',
        'https://ibuild.yzw.cn/api/downloadCenter/query?t=/1632808991778',
        'https://ibuildreport.yzw.cn/org/#/home',
        'https://ibuild.yzw.cn/mgt/#/organization/settings',
        'https://ibuild.yzw.cn/mgt/#/organizationPrint',
        'https://ibuild.yzw.cn/open/#/',
        'https://ibuild.yzw.cn/open/#/order',
        'https://ibuild.yzw.cn/open/#/productMgt/hardwareDetail?sysNo=10807',
        'https://ibuild.yzw.cn/open/#/downloadCenter',
        'https://ibuild.yzw.cn/api/config/getConfig/?t=/1632810299561',
        'https://ibuild.yzw.cn/mgt/#/project/edit/20859',
        'https://ibuild.yzw.cn/api/pm/security/securityCheck/10142/detail/127649?t=/1632815878833',
        'https://ibuild.yzw.cn/api/pm/quality/qualityCheck/10142/detail/31700?t=/1632815560420',
        'https://ibuild.yzw.cn/api/pm/quality/qualityCheck/10142/detail/31700?t=/1632815560420',
        'https://ibuild.yzw.cn/api/project/videoRecord/detail/15007?t=/1632818982730',
        'https://ibuild.yzw.cn/mgt/#/project/edit/20859',
        'https://ibuild.yzw.cn/mgt/#/project/10142',
        'https://ibuild.yzw.cn/mgt/#/project/projectSiteMap/16756',
        'https://ibuild.yzw.cn/mgt/#/project/projectLargeScreen/16756',
        'https://ibuild.yzw.cn/mgt/#/project/screenSettings/16756',
        'https://ibuild.yzw.cn/mgt/#/project/projectConfigManage/16756',
        'https://ibuild.yzw.cn/mgt/#/project/projectSetting/16756/appConfig/14'
    ]

if __name__=='__main__':
    env='qa'
    if env=='qa':
        new_sites=[]
        for site in sites:
            site=site.replace('https://ibuild.yzw.cn','http://ibuild.yzw.cn.qa:81')
            new_sites.append(site)
    sites=new_sites
    driver=webdriver.Chrome()
    driver.get('http://ibuild.yzw.cn.qa:81/')
    driver.add_cookie({'name':'web.auth.yzw','value':'5BA9EBFCBF34CBE7371122427E4A945A5F7FAC5C754F74F7DF1445A7B898A639C3D4DA4E5B8DC4016A3779B1E3F348CB1B2C7E278EB94AD96F3E830A128850D52D12505FAD5D79ED4D38FCB2A358CA63A391EEBE6063D0ADA0F999A7315517E7F224C5CFCC2572CD42C9E1B2230F44A9A407518717C7D2571994433C79D82A74D496AB4DDDD70DAE394119DD46C9A5EA18E2B637321F0D71712EA694694C9F7B0C07B6B8F120801B137BF439EC4E3E6B21DBE6F2AB7B18A66D40CA086AF293E414530466103699F0C8B729EF2E496B028B03C16328AA791DB083DA39506D2199E0DA891171BA812141C0E36D332E2FF285E3E229AAE3E19FFFC3CF47B0883E29C0A31F04A769EFF00EF8245233DF6277A53DD77B359886B4C051F3766CAC395A3C75F5ADE05CB2B99FB1D41CB4C9FA940CE53869190386C69EF27CAC6A008D32E22712567EDA0E4288667EF090B8E57E48FCA905301723210BD746317C5BA57671480CD0BCB84B172C8BB824B3AE86A5CD812929854B9844E3D2C23E31E2044EB46D32DF13B007DF10C1EE5538B50AC7F008D69E9B7D7E717085152D2F3536FF94F75C461FFBD321ABF942BC999660E5F956971770063482D2EA916F82707DD148F46B7002375F53F91E3F89668A4ED6C8056FE202DE614E87D4C2AD282B2E46D183EA1B87E99389BF4A2A5280F309C31E38D8FB77EFF24BFFEF754F10427D6BEA5DC0346E3833D0DDE165E39F67D1C98CA9596D4D243A5ADE7E3432C0276B8528262B6B57CDA7EACF488AA93254DF043A097B6454FEEC11C5ABB427F3D3A172FF658DEFE47581E05F56D9392C6FE68A94E95D59D2657EC75CAF9BBF8F5A1469C83B251CB8B393D0697CBA0D5441288C09956E1EC8D3606F48B089F50CF51156E3B211D20A9EC0BFF801891CD97B5DC7DDDBD9DD68920FCE8C3AAFDB8F4974EF3644758F44C037B64B6C97E985008C5D34CC5245150A2243EA9767EDA13E082AD292B98928A1'})
    
    for site in sites:
        driver.get(site)
        driver.implicitly_wait(2)
        # driver.switch_to()
        elements=driver.find_elements_by_css_selector("img[src^='http'")
        print('site:%s' % site)
        for el in iter(elements):
            src=el.get_attribute('src')
            print(src)
            if('oss.yzw.cn' in src):
                print('Fail\033[0m')
    driver.close()