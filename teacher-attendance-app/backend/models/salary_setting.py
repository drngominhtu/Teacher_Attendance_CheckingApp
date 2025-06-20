from database import db
from datetime import datetime

class SalarySetting(db.Model):
    __tablename__ = 'salary_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(50), unique=True, nullable=False)
    setting_value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert salary setting to dictionary"""
        return {
            'id': self.id,
            'setting_key': self.setting_key,
            'setting_value': self.setting_value,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_setting(key, default_value=None):
        """Get setting value by key"""
        try:
            setting = SalarySetting.query.filter_by(setting_key=key, is_active=True).first()
            return setting.setting_value if setting else default_value
        except:
            return default_value
    
    @staticmethod
    def set_setting(key, value, description=None):
        """Set setting value"""
        try:
            setting = SalarySetting.query.filter_by(setting_key=key).first()
            if setting:
                setting.setting_value = str(value)
                setting.description = description
                setting.updated_at = datetime.utcnow()
            else:
                setting = SalarySetting(
                    setting_key=key,
                    setting_value=str(value),
                    description=description
                )
                db.session.add(setting)
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error setting salary setting: {e}")
            return False
