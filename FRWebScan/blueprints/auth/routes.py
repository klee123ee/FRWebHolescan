from flask import render_template, redirect, url_for, session, request, flash, jsonify
from . import auth_bp
from models import db, User, OperLog

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            # 记录登录日志
            oper_log = OperLog(
                oper_type='登录',
                oper_content='用户登录成功',
                oper_ip=request.remote_addr,
                oper_status='成功',
                user_id=user.id
            )
            db.session.add(oper_log)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('用户名或密码错误')
            return redirect(url_for('auth.login'))
    return render_template('/auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('两次输入的密码不一致')
            return redirect(url_for('auth.register'))
            
        if len(password) < 8:
            flash('密码长度至少需要8个字符')
            return redirect(url_for('auth.register'))
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('用户名已存在')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'注册失败：{str(e)}')
            return redirect(url_for('auth.register'))

    return render_template('/auth/register.html')

@auth_bp.route('/logout')
def logout():
    if 'username' in session:
        # 记录登出日志
        oper_log = OperLog(
            oper_type='登出',
            oper_content='用户登出成功',
            oper_ip=request.remote_addr,
            oper_status='成功',
            user_id=User.query.filter_by(username=session['username']).first().id
        )
        db.session.add(oper_log)
        db.session.commit()
    session.pop('username', None)
    return redirect(url_for('auth.login'))

@auth_bp.route('/resetpassword', methods=['GET', 'POST'])
def resetpassword():
    if 'username' not in session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'code': 1, 'msg': '请先登录'})
        flash('请先登录')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # 获取当前用户
        user = User.query.filter_by(username=session['username']).first()
        
        # 验证旧密码
        if not user.check_password(old_password):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'code': 1, 'msg': '旧密码错误'})
            flash('旧密码错误')
            return redirect(url_for('auth.resetpassword'))
        
        # 验证新密码和确认密码是否一致
        if new_password != confirm_password:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'code': 1, 'msg': '新密码和确认密码不一致'})
            flash('新密码和确认密码不一致')
            return redirect(url_for('auth.resetpassword'))
        
        # 验证新密码长度
        if len(new_password) < 6:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'code': 1, 'msg': '新密码长度不能少于6个字符'})
            flash('新密码长度不能少于6个字符')
            return redirect(url_for('auth.resetpassword'))
        
        try:
            # 更新密码
            user.set_password(new_password)
            
            # 记录密码重置日志
            oper_log = OperLog(
                oper_type='重置密码',
                oper_content='用户重置密码成功',
                oper_ip=request.remote_addr,
                oper_status='成功',
                user_id=user.id
            )
            db.session.add(oper_log)
            db.session.commit()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'code': 0, 'msg': '密码重置成功'})
            flash('密码重置成功')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'code': 1, 'msg': f'密码重置失败：{str(e)}'})
            flash(f'密码重置失败：{str(e)}')
            return redirect(url_for('auth.resetpassword'))
    
    return render_template('/auth/resetpassword.html')