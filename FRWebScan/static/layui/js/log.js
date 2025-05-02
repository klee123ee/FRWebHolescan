layui.use(['element', 'form', 'laydate', 'layer'], function () {
    var element = layui.element;
    var form = layui.form;
    var laydate = layui.laydate;
    var layer = layui.layer;

    // 清空日志按钮点击事件
    $('button[lay-filter="searchLog"]').on('click', function(){
        layer.confirm('确定要清空所有日志吗？(无法恢复)', {
            icon: 3,
            title: '操作警告！',
            btn: ['确定','取消']
        }, function(index){
            // 用户点击确定后的操作
            layer.close(index);
            $.ajax({
                url: '/clear_logs',
                method: 'POST',
                success: function(res) {
                    if (res.success) {
                        layer.msg('日志已清空', {icon: 1});
                        setTimeout(function() {
                            location.reload();
                        }, 1500);
                    } else {
                        layer.msg('清空日志失败：' + res.message, {icon: 2});
                    }
                },
                error: function() {
                    layer.msg('请求失败，请检查网络', {icon: 2});
                }
            });
        });
    });
});