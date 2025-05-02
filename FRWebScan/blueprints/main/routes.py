from flask import render_template, redirect, url_for, session
from . import main_bp

@main_bp.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('auth.login'))

# 漏洞扫描相关路由
@main_bp.route('/newscan')
def newscan():
    if 'username' in session:
        return render_template('Hole_Scan/new_scan.html')
    return redirect(url_for('auth.login'))

@main_bp.route('/scanlist')
def scanlist():
    if 'username' in session:
        return render_template('Hole_Scan/scan_task.html')
    return redirect(url_for('auth.login'))

# 资产管理相关路由

# 渗透测试相关路由
@main_bp.route('/pentest')
def pentest():
    if 'username' in session:
        return render_template('Pentest/pentest.html')
    return redirect(url_for('auth.login'))

@main_bp.route('/shell')
def shell():
    if 'username' in session:
        return render_template('Pentest/shell.html')
    return redirect(url_for('auth.login'))

@main_bp.route('/exploit')
def exploit():
    if 'username' in session:
        return render_template('Pentest/exploit.html')
    return redirect(url_for('auth.login'))

# 安全工具相关路由
@main_bp.route('/subdomain')
def subdomain():
    if 'username' in session:
        return render_template('Tools/subdomain.html')
    return redirect(url_for('auth.login'))

@main_bp.route('/dirscan')
def dirscan():
    if 'username' in session:
        return render_template('Tools/dirscan.html')
    return redirect(url_for('auth.login'))

@main_bp.route('/fuzz')
def fuzz():
    if 'username' in session:
        return render_template('Tools/fuzz.html')
    return redirect(url_for('auth.login'))

@main_bp.route('/encode')
def encode():
    if 'username' in session:
        return render_template('Tools/encode.html')
    return redirect(url_for('auth.login'))

# 报告管理相关路由
@main_bp.route('/report')
def report():
    if 'username' in session:
        return render_template('Report/report.html')
    return redirect(url_for('auth.login'))

@main_bp.route('/template')
def template():
    if 'username' in session:
        return render_template('Report/template.html')
    return redirect(url_for('auth.login'))

# 系统设置相关路由
@main_bp.route('/user')
def user():
    if 'username' in session:
        return render_template('Settings/user.html')
    return redirect(url_for('auth.login'))

@main_bp.route('/role')
def role():
    if 'username' in session:
        return render_template('Settings/role.html')
    return redirect(url_for('auth.login'))

@main_bp.route('/log')
def log():
    if 'username' in session:
        return render_template('Settings/log.html')
    return redirect(url_for('auth.login'))

@main_bp.route('/setting')
def setting():
    if 'username' in session:
        return render_template('Settings/setting.html')
    return redirect(url_for('auth.login'))