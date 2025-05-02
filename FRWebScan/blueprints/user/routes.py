from flask import render_template, redirect, url_for, session, request, flash, jsonify
from . import user_bp
from models import db, User, OperLog

@user_bp.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return render_template('/user/profile.html')

@user_bp.route('/profile/log')
def log():
    if 'username' not in session:
        flash('请先登录', 'error')
        return redirect(url_for('auth.login'))
    username = session['username']
    user = User.query.filter_by(username=username).first()
    logs = OperLog.query.filter_by(user_id=user.id).all()
    return render_template('/user/log.html', user=user, logs=logs)

@user_bp.route('/clear_logs', methods=['POST'])
def clear_logs():
    if 'username' not in session:
        return jsonify(success=False, message='未登录')
    
    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return jsonify(success=False, message='用户不存在')

    try:
        OperLog.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        return jsonify(success=True)
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=str(e)) 