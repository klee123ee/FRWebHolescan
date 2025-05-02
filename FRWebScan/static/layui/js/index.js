layui.use(['element', 'form', 'jquery', 'table'], function(){
        var element = layui.element;
        var form = layui.form;
        var $ = layui.jquery;
        var table = layui.table;

        // 监听左侧导航菜单点击事件
        $('.layui-side .layui-nav-child a').on('click', function(e){
            e.preventDefault();
            var url = $(this).attr('data-url');
            if(url){
                // 移除所有active类
                $('.layui-side .layui-nav-child a').removeClass('active');
                // 当前菜单项添加active类
                $(this).addClass('active');

                // 切换标签页
                var tabTitle = $(this).text();
                var tabId = url;

                // 检查标签页是否已存在
                if($('.layui-tab-title li[lay-id="' + tabId + '"]').length === 0){
                    // 添加新标签页
                    element.tabAdd('mainTabs', {
                        title: '<i class="' + $(this).find('i').attr('class') + '"></i> ' + tabTitle,
                        content: $('#' + tabId).html(),
                        id: tabId
                    });
                }

                // 切换到对应标签页
                element.tabChange('mainTabs', tabId);
            }
        });

        // 监听标签页删除事件
        element.on('tabDelete(mainTabs)', function(data){
            // 移除对应的导航菜单active类
            $('.layui-side .layui-nav-child a[data-url="' + data.id + '"]').removeClass('active');
        });

        // 页面加载时设置当前选中项
        var currentUrl = window.location.pathname;
        if(currentUrl === '/'){
            currentUrl = 'dashboard';
        } else {
            currentUrl = currentUrl.split('/').pop();
        }

        // 设置导航菜单选中状态
        $('.layui-side .layui-nav-child a[data-url="' + currentUrl + '"]').addClass('active');

        // 保持父菜单展开状态
        if($('.layui-side .layui-nav-child a.active').length > 0){
            $('.layui-side .layui-nav-child a.active').parents('.layui-nav-item').addClass('layui-nav-itemed');
        }

        // 表单提交
        form.on('submit(emailForm)', function(data){
            // 处理邮箱设置表单提交
            layer.msg('邮箱设置已保存');
            return false;
        });

        form.on('submit(dingtalkForm)', function(data){
            // 处理钉钉设置表单提交
            layer.msg('钉钉设置已保存');
            return false;
        });
    });